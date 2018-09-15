# Third-party imports.
from django_filters.rest_framework import CharFilter, FilterSet

# Local imports.
from .models import Recipe

__author__ = 'Jason Parent'


class RecipeSearchFilterSet(FilterSet):
    query = CharFilter(help_text='A search query.', method='filter_query')

    def filter_query(self, queryset, name, value):
        return queryset.search(value)

    class Meta:
        model = Recipe
        fields = ('query',)
