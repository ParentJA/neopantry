from django_filters.rest_framework import CharFilter, FilterSet

from .models import Recipe, RecipeSearchWord


class RecipeSearchFilterSet(FilterSet):
    query = CharFilter(help_text='A search query.', method='filter_query')

    def filter_query(self, queryset, name, value):
        return queryset.search(value)

    class Meta:
        model = Recipe
        fields = ('query',)


class RecipeSearchWordFilterSet(FilterSet):
    query = CharFilter(method='filter_query')

    def filter_query(self, queryset, name, value):
        return queryset.search(value)

    class Meta:
        model = RecipeSearchWord
        fields = ('query',)
