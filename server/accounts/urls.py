from django.urls import path

from .views import LogInView, LogOutView, ProfileView, SignUpView


urlpatterns = [
    path('log-in/', LogInView.as_view(), name='log-in'),
    path('log-out/', LogOutView.as_view(), name='log-out'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('profile/', ProfileView.as_view(), name='profile'),
]