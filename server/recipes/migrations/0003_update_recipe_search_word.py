from django.contrib.postgres.operations import TrigramExtension
from django.db import connection, migrations


def update_recipe_search_word(apps, schema_editor):
    sql = """
        INSERT INTO recipes_recipesearchword (word)
        SELECT word FROM ts_stat('
          SELECT to_tsvector(''simple'', name) ||
                 to_tsvector(''simple'', coalesce(description, ''''))
            FROM recipes_recipe
        ');
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_remove_recipesearchword_recipe_and_more'),
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
