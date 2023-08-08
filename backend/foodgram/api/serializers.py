from django.db import transaction
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import (FavoriteRecipe, Ingredient, ShoppingCart, Recipe,
                            Tag, RecipeIngredient)
from users.models import User, Subscribe


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class UserReadSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return obj.subscriber.filter(author=obj).exists()


class SubscriptionSerializer(UserReadSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'recipes', 'recipes_count', 'is_subscribed')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data


class SubscribeAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = (
            'user',
            'author',
        )

    def validate(self, obj):
        user = self.context['request'].user
        author = obj['author']
        if user == author:
            raise serializers.ValidationError('Нельзя подписаться на себя')
        if Subscribe.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError('Подписка уже оформлена')
        return obj


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ('id', 'user', 'recipe')


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('id', 'user', 'recipe')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measure')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measure'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measure', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = UserReadSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')

    def validate_ingredients(self, value):
        ingredients_list = value['ingredients']

        if not ingredients_list:
            raise ValidationError({
                'ingredients': 'В рецепте отсутствуют ингредиенты!'})
        used_ingredients = set()
        for ingredient in ingredients_list:
            if int(ingredient['amount']) < 1:
                raise ValidationError(
                    'Минимальное количество ингредиентов - 1')
            used_ingredients.add(ingredient['id'])
        if len(used_ingredients) != len(ingredients_list):
            raise ValidationError('Ингредиент не должен повторяться!')
        return value

    def validate_tags(self, value):
        tag_count = Tag.objects.count()
        if not value or len(value) > tag_count:
            raise ValidationError(
                f'Количество тегов должно быть от 1 до {tag_count}.'
            )
        if len(value) != len(set(value)):
            raise ValidationError('Теги не должны повторяться!')
        return value

    def create_or_update(self, validated_data, object):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        object.tags.set(tags)
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(Ingredient,
                                                   id=ingredient.get('id'))
            RecipeIngredient.objects.bulk_create(
                ingredient=current_ingredient,
                recipe=object,
                amount=ingredient.get('amount')
            )
        return

    @transaction.atomic
    def create(self, validated_data):
        author = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data, author=author)
        self.create_or_update(self, validated_data, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.ingredients.clear()
        self.create_or_update(self, validated_data, instance)
        instance.save()
        return instance
