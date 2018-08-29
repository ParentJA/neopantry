# Third-party imports.
from phonenumber_field.modelfields import PhoneNumberField

# Django imports.
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

__author__ = 'Jason Parent'


class User(AbstractUser):
    photo = models.ImageField(upload_to='photos', default='photos/no-image.jpg', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    @staticmethod
    def autocomplete_search_fields():
        return 'username__icontains', 'email__icontains', 'first_name__icontains', 'last_name__icontains',

    @property
    def photo_url(self):
        try:
            return self.photo.url
        except ValueError:
            return None
