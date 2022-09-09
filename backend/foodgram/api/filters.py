import django_filters
from django_filters.widgets import BooleanWidget

from recipes.models import Ingredient, Recipe


class IngredientFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class ResipeFilter(django_filters.FilterSet):

    is_favorite = django_filters.BooleanFilter(
        field_name='is_favorite',
        method='favorite_filter',
        widget=BooleanWidget
    )

    is_in_shopping_cart = django_filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='shopping_cart_filter',
        widget=BooleanWidget
    )

    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')

    def favorite_filter(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def shopping_cart_filter(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return Recipe.objects.filter(shoppinglist__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)
