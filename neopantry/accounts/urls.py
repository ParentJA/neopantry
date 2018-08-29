# Django imports.
from django.urls import path

# Local imports.
from .views import LogInView, LogOutView, SignUpView

__author__ = 'Jason Parent'

urlpatterns = [
    path('log-in/', LogInView.as_view(), name='log-in'),
    path('log-out/', LogOutView.as_view(), name='log-out'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
]
