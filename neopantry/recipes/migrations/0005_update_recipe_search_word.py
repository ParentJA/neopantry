# Django imports.
from django.contrib.postgres.operations import TrigramExtension
from django.db import connection, migrations

__author__ = 'Jason Parent'


def update_recipe_search_word(apps, schema_editor):
    Recipe = apps.get_model('recipes', 'Recipe')
    queries = [f"""
        INSERT INTO recipes_recipesearchword (recipe_id, word)
        SELECT {recipe.id}, word FROM ts_stat('
          SELECT to_tsvector(''simple'', name) ||
                 to_tsvector(''simple'', description)
            FROM recipes_recipe
           WHERE id = {recipe.id}
        ');
    """ for recipe in Recipe.objects.all()]
    if queries:
        with connection.cursor() as cursor:
            cursor.execute('\n'.join(queries))


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0004_auto_20180915_0309'),
    ]
    operations = [
        TrigramExtension(),
        migrations.RunSQL(sql="""
            CREATE INDEX IF NOT EXISTS recipe_search_word_trigram_index
                ON recipes_recipesearchword
             USING gin (word gin_trgm_ops);
        """, elidable=True),
        migrations.RunPython(update_recipe_search_word, elidable=True),
    ]
