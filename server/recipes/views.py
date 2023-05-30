from django.db import transaction
from django.db.models import F, Prefetch

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets

from .models import Ingredient, Recipe, RecipeNote, RecipeReview, RecipeSearchWord, UserRecipe
from .filters import RecipeSearchFilterSet, RecipeSearchWordFilterSet
from .pagination import RecipePagination
from .permissions import IsResourceOwner
from .serializers import (
    RecipeSerializer, 
    RecipeNoteSerializer, 
    RecipeReviewSerializer, 
    RecipeSearchSerializer, 
    RecipeSearchWordSerializer,
    UserRecipeSerializer,
    UserRecipeSearchSerializer,
)


class RecipeSearchView(generics.ListAPIView):
    filterset_class = RecipeSearchFilterSet
    pagination_class = RecipePagination
    queryset = Recipe.objects.all()
    serializer_class = RecipeSearchSerializer


class RecipeSearchWordsView(generics.ListAPIView):
    queryset = RecipeSearchWord.objects.all()
    serializer_class = RecipeSearchWordSerializer
    filterset_class = RecipeSearchWordFilterSet


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


class UserNoteView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsResourceOwner,)
    queryset = RecipeNote.objects.all()
    serializer_class = RecipeNoteSerializer


class UserNoteByIdView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsResourceOwner,)
    queryset = RecipeNote.objects.all()
    serializer_class = RecipeNoteSerializer


class RecipeReviewView(generics.ListCreateAPIView):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('recipe', 'user',)
    permission_classes = (permissions.IsAuthenticated, IsResourceOwner,)
    queryset = RecipeReview.objects.select_related('recipe', 'user').all()
    serializer_class = RecipeReviewSerializer


class RecipeReviewByIdView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsResourceOwner,)
    queryset = RecipeReview.objects.select_related('recipe', 'user').all()
    serializer_class = RecipeReviewSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            # Update recipe.
            recipe = instance.recipe
            recipe.total_make_again -= (1 if instance.make_again else 0)
            recipe.total_ratings -= instance.rating
            recipe.num_reviews -= 1
            recipe.save()

            # Delete review.
            instance.delete()


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
