# Django imports.
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F, Prefetch

# Third-party imports.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, exceptions, permissions, response, status, views, viewsets
from rest_framework.response import Response

# Local imports.
from .models import Ingredient, Recipe, RecipeNote, RecipeReview, UserRecipe
from .pagination import RecipePagination
from .permissions import IsResourceOwner
from .serializers import (
    RecipeSerializer, RecipeNoteSerializer, RecipeReviewSerializer,
    ReadUserRecipeSerializer, WriteUserRecipeSerializer, RecipeSearchSerializer, UserRecipeSerializer,
    UserRecipeSearchSerializer
)

__author__ = 'Jason Parent'


class RecipeSearchView(generics.ListAPIView):
    pagination_class = RecipePagination
    serializer_class = RecipeSearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query')
        if query is None:
            return Recipe.objects.all()
        search_query = SearchQuery(query)
        return Recipe.objects.annotate(
            rank=SearchRank(F('search_vector'), search_query)
        ).filter(
            rank__gte=0.1
        ).order_by('-rank')


class RecipeView(generics.RetrieveAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return Recipe.objects.prefetch_related(
            Prefetch('ingredients', queryset=Ingredient.objects.select_related('food').order_by('rank'))
        )


class RecipeNoteView(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('recipe',)
    permission_classes = (permissions.IsAuthenticated, IsResourceOwner,)
    serializer_class = RecipeNoteSerializer

    def get_queryset(self):
        return RecipeNote.objects.filter(user=self.request.user)


class RecipeReviewView(generics.ListCreateAPIView):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('recipe', 'user',)
    permission_classes = (permissions.IsAuthenticated, IsResourceOwner,)
    queryset = RecipeReview.objects.select_related('recipe', 'user').all()
    serializer_class = RecipeReviewSerializer

    def perform_create(self, serializer):
        recipe_review = serializer.save()

        # Update recipe.
        recipe = recipe_review.recipe
        recipe.total_make_again += (1 if recipe_review.make_again else 0)
        recipe.total_ratings += recipe_review.rating
        recipe.num_reviews += 1
        recipe.save()


# class UserRecipeView(views.APIView):
#     def get(self, *args, **kwargs):
#         user_pk = self.kwargs['user_pk']
#         if self.request.user.id != int(user_pk):
#             raise exceptions.PermissionDenied()
#         user_recipes = UserRecipe.objects.select_related('user', 'recipe').filter(user__pk=user_pk)
#         return response.Response(
#             status=status.HTTP_200_OK,
#             data=ReadUserRecipeSerializer(user_recipes, many=True).data
#         )
#
#     def post(self, *args, **kwargs):
#         user_pk = self.kwargs['user_pk']
#         if self.request.user.id != int(user_pk):
#             raise exceptions.PermissionDenied()
#         serializer = WriteUserRecipeSerializer(data={'user': user_pk, 'recipe': self.request.data['recipe']})
#         serializer.is_valid(raise_exception=True)
#         user_recipe = serializer.save()
#         return response.Response(
#             status=status.HTTP_201_CREATED,
#             data=ReadUserRecipeSerializer(user_recipe).data
#         )
#
#     def delete(self, *args, **kwargs):
#         user_pk = self.kwargs['user_pk']
#         if self.request.user.id != int(user_pk):
#             raise exceptions.PermissionDenied()
#         user_recipe = generics.get_object_or_404(UserRecipe, user_id=user_pk, recipe_id=self.kwargs['recipe_pk'])
#         user_recipe.delete()
#         return response.Response(status=status.HTTP_204_NO_CONTENT, data=None)


class UserRecipeView(generics.RetrieveDestroyAPIView):
    pagination_class = RecipePagination
    permission_classes = (permissions.IsAuthenticated, IsResourceOwner,)
    queryset = UserRecipe.objects.select_related('user', 'recipe')
    serializer_class = UserRecipeSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {
            'user__pk': self.kwargs['user_pk'],
            'recipe__pk': self.kwargs['recipe_pk']
        }
        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class UserRecipeSearchView(generics.ListCreateAPIView):
    pagination_class = RecipePagination
    permission_classes = (permissions.IsAuthenticated, IsResourceOwner,)
    queryset = UserRecipe.objects.select_related('user', 'recipe').order_by('id')
    serializer_class = UserRecipeSearchSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(user__pk=self.kwargs['user_pk'])
