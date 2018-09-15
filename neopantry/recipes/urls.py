# Django imports.
from django.urls import path

# Local imports.
from .views import (
    RecipeView, RecipeNoteView, RecipeReviewView, UserRecipeView, RecipeSearchView, UserRecipeSearchView
)

__author__ = 'Jason Parent'

urlpatterns = [
    path('notes/<int:pk>/', RecipeNoteView.as_view({
        'get': 'retrieve',
        'put': 'partial_update',
        'delete': 'destroy',
    }), name='recipe-note-detail'),
    path('notes/', RecipeNoteView.as_view({
        'get': 'list',
        'post': 'create',
    }), name='recipe-note-list'),
    path('reviews/', RecipeReviewView.as_view(), name='recipe-review'),
    path('users/<int:user_pk>/recipes/<int:recipe_pk>/', UserRecipeView.as_view(), name='user-recipe'),
    path('users/<int:user_pk>/recipes/', UserRecipeSearchView.as_view(), name='user-recipe-search'),
    # path('users/<int:user_pk>/notes/<int:note_pk>/', UserNoteByIdView.as_view(), name='user-note-by-id'),
    # path('users/<int:user_pk>/notes/', UserNoteView.as_view(), name='user-note'),
    path('<int:pk>/', RecipeView.as_view(), name='recipe'),
    path('', RecipeSearchView.as_view(), name='recipe-search'),
]
