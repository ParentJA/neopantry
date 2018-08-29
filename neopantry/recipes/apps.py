# Django imports.
from django.apps import AppConfig

__author__ = 'Jason Parent'


class RecipeConfig(AppConfig):
    name = 'recipes'

    def ready(self):
        import recipes.signals
