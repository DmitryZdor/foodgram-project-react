from django.contrib.admin import ModelAdmin, site

from recipes import models


class RecipeAdmin(ModelAdmin):
    list_display = ['name', 'author', ]
    fields = ['name', 'author', 'text', 'image',
              'cooking_time', 'in_favorite']
    readonly_fields = ['in_favorite', ]
    list_filter = ['name', 'author', 'tags']

    def in_favorite(self, obj):
        return models.Favorite.objects.filter(recipe=obj).count()


site.register(models.Tag)
site.register(models.Recipe, RecipeAdmin)
site.register(models.RecipeIngredient)
site.register(models.ShoppingList)
site.register(models.Ingredient)
site.register(models.Favorite)
site.register(models.RecipeTag)
