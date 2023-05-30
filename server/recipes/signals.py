from django.contrib.postgres.search import SearchVector
from django.db import connection
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import RecipeSearchWord


@receiver(post_save, sender='recipes.Recipe', dispatch_uid='on_recipe_save')
def update_search_vector(sender, instance, *args, **kwargs):
    # Handle recipe search vector.
    sender.objects.filter(pk=instance.id).update(search_vector=(
        SearchVector('name', weight='A') +
        SearchVector('description', weight='B') + 
        SearchVector('ingredients_text', weight='B')
    ))

    # Handle search words.
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO recipes_recipesearchword (word)
            SELECT word FROM ts_stat('
                SELECT to_tsvector(''simple'', name) ||
                       to_tsvector(''simple'', coalesce(description, '''')) ||
                       to_tsvector(''simple'', coalesce(ingredients_text, ''''))
                FROM recipes_recipe
                WHERE id = '%s'
            ')
            ON CONFLICT (word) DO NOTHING;
        """, [str(instance.id),])
