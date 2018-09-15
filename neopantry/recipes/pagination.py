# Third-party imports.
from rest_framework import pagination

__author__ = 'Jason Parent'


class RecipePagination(pagination.PageNumberPagination):
    page_size = 25
