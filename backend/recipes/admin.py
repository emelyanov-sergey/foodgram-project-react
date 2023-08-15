from django.contrib.admin import register, ModelAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient


@register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin, ModelAdmin):
    resource_classes = [IngredientResource]
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('id', 'name', 'author', 'text')
    list_filter = ('author', 'name', 'tags')

    @staticmethod
    def favorites(obj):
        return obj.favorites.count()


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe')


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('user', 'recipe')
