# Django imports.
from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver

__author__ = 'Jason Parent'


@receiver(post_save, sender='recipes.Recipe')
def update_search_vector(sender, instance, *args, **kwargs):
    sender.objects.filter(pk=instance.id).update(search_vector=(
        SearchVector('name', weight='A') +
        SearchVector('description', weight='B')
    ))
