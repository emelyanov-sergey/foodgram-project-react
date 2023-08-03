from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


TAG = [
    ('Завтрак', ('#E26C2D', 'breakfast')),
    ('Обед', ('#49B64E', 'breakfast')),
    ('Ужин', ('#3d66bf', 'dinner'))
]

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=15,
        verbose_name='тэг',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )
    color = models.CharField(
        max_length=16,
        verbose_name='Цвет',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Слаг',
        help_text='Обязательное поле',
        unique=True,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )
    measure = models.CharField(
        max_length=15,
        verbose_name='Единицы измерения',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Обязательное поле'
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Обязательное поле',
        blank=False,
        null=False
    )
    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Обязательное поле',
        blank=True,
        null=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='RecipeIngredient',
        verbose_name='Список ингредиентов',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах',
        help_text='Обязательное поле',
        default=0,
        blank=False,
        null=False,
        validators=[
            MinValueValidator(
                1, 'Время приготовления должно быть больше 1 минуты'
            )
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'Рецепт: {self.name}. Автор: {self.author.username}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField('Количество',)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Количество ингредиентов в рецепте'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в избраннное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (f'{self.user.username} добавил'
                f'{self.recipe.name} в список покупок')
