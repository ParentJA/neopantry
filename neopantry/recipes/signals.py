# Django imports.
from django.contrib.postgres.search import SearchVector
from django.db import connection
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

# Local imports.
from .models import RecipeSearchWord

__author__ = 'Jason Parent'


@receiver(post_save, sender='recipes.Recipe')
def update_search_vector(sender, instance, *args, **kwargs):
    # Handle recipe search vector.
    sender.objects.filter(pk=instance.id).update(search_vector=(
        SearchVector('name', weight='A') +
        SearchVector('description', weight='B')
    ))

    # Handle search words.
    RecipeSearchWord.objects.filter(recipe_id=instance.id).delete()
    with connection.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO recipes_recipesearchword (recipe_id, word)
            SELECT {instance.id}, word FROM ts_stat('
            SELECT to_tsvector(''simple'', name) ||
                   to_tsvector(''simple'', description)
                FROM recipes_recipe
               WHERE id = {instance.id}
            ');
        """)


@receiver(post_delete, sender='recipes.Recipe')
def on_post_delete(sender, instance, *args, **kwargs):
    # Handle search words.
    RecipeSearchWord.objects.filter(recipe_id=instance.id).delete()
