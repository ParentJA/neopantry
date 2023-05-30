from django.urls import path

from .views import (
    RecipeView, 
    RecipeNoteView, 
    RecipeReviewByIdView, 
    RecipeReviewView, 
    UserRecipeView, 
    RecipeSearchView,
    RecipeSearchWordsView,
    UserRecipeSearchView,
)

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
    path('reviews/<int:pk>/', RecipeReviewByIdView.as_view(), name='recipe-review-by-id'),
    path('reviews/', RecipeReviewView.as_view(), name='recipe-review'),
    path('users/<int:user_pk>/recipes/<int:recipe_pk>/', UserRecipeView.as_view(), name='user-recipe'),
    path('users/<int:user_pk>/recipes/', UserRecipeSearchView.as_view(), name='user-recipe-search'),
    # path('users/<int:user_pk>/notes/<int:note_pk>/', UserNoteByIdView.as_view(), name='user-note-by-id'),
    # path('users/<int:user_pk>/notes/', UserNoteView.as_view(), name='user-note'),
    path('recipe-search-words/', RecipeSearchWordsView.as_view(), name='recipe-search-words'),
    path('<int:pk>/', RecipeView.as_view(), name='recipe'),
    path('', RecipeSearchView.as_view(), name='recipe-search'),
]
