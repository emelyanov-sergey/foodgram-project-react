from django.db.models import F, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from djoser.views import UserViewSet


from recipes.models import (
    Ingredient,
    Recipe,
    FavoriteRecipe,
    RecipeIngredient,
    Tag, ShoppingCart
)
from users.models import Subscribe, User
from api.filters import IngredientFilter, RecipeFilter
from api.mixins import CreateDeleteMixin
from api.pagination import PageNumberPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CustomUserCreateSerializer,
                             SubscriptionSerializer,
                             TagSerializer, IngredientSerializer,
                             RecipeCreateSerializer, FavoriteSerializer,
                             ShoppingCartSerializer)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer()
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    @action(detail=True, methods=['POST', 'DELETE'])
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            serializer = SubscriptionSerializer(author,
                                                data=request.data,
                                                context={'request': request})
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        get_object_or_404(Subscribe, user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def subscriptions(self, request):
        return self.paginate_queryset(
            SubscriptionSerializer(
                self.paginate_queryset(
                    User.objects.filter(following__user=request.user)
                ),
                many=True,
                context={'request': request},
            ).data
        )


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(CreateDeleteMixin, ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer()
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    @action(detail=True,
            methods=['POST'],
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        return self.creata_odj(FavoriteSerializer, data, request)

    @favorite.mapping.delete
    def unfavorite(self, request, pk):
        return self.delete_obj(FavoriteRecipe, user=request.user, recipe=pk)

    @action(detail=True,
            methods=['POST'],
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        return self.creata_odj(ShoppingCartSerializer, data, pk)

    @shopping_cart.mapping.delete
    def remove_from_cart(self, request, pk):
        return self.delete_obj(ShoppingCart, user=request.user, recipe=pk)

    @action(detail=False,
            methods=['get'],
            permission_classes=(IsAuthenticated,)
            )
    def download_shopping_cart(self, request):
        shopping_cart_recipes = (ShoppingCart.objects.
                                 filter(user=request.user).
                                 values_list('recipe', flat=True))
        ingredients = (RecipeIngredient.objects
                       .filter(recipe__in=shopping_cart_recipes)
                       .values(name=F('ingredient__name'),
                               unit=F('ingredient__measurement_unit'))
                       .annotate(amount_sum=Sum('amount'))
                       ).order_by('name')
        shopping_cart = '\n'.join([
            f'{ingredient["name"]} - {ingredient["unit"]} '
            f'{ingredient["amount_sum"]}'
            for ingredient in ingredients
        ])
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping-cart.txt"')
        response.write(shopping_cart)
        return response
