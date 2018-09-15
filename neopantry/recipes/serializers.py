# Third-party imports.
from rest_framework import serializers

# Local imports.
from .models import Food, Ingredient, Recipe, RecipeNote, RecipeReview, UserRecipe

__author__ = 'Jason Parent'


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'name',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'description', 'rank', 'is_optional',)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'description', 'ingredients', 'instructions', 'photo', 'average_make_again',
            'average_rating', 'num_reviews',
        )


class RecipeSearchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'photo', 'average_rating', 'num_reviews',)


class RecipeNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeNote
        fields = ('id', 'recipe', 'user', 'note', 'created_ts', 'updated_ts',)
        read_only_fields = ('id', 'created_ts', 'updated_ts',)


class RecipeReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = RecipeReview
        fields = ('id', 'recipe', 'user', 'make_again', 'rating', 'review', 'username',)
        read_only_fields = ('id', 'username',)


class ReadUserRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeSearchSerializer(read_only=True)

    class Meta:
        model = UserRecipe
        fields = ('id', 'user', 'recipe',)


class WriteUserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecipe
        fields = ('id', 'user', 'recipe',)


class UserRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = UserRecipe
        fields = ('id', 'user', 'recipe',)


class UserRecipeSearchSerializer(serializers.ModelSerializer):
    recipe = RecipeSearchSerializer()

    def create(self, validated_data):
        recipe = Recipe.objects.get(**validated_data.pop('recipe'))
        return UserRecipe.objects.create(**{'recipe': recipe, **validated_data})

    def update(self, instance, validated_data):
        raise NotImplementedError()

    class Meta:
        model = UserRecipe
        fields = ('id', 'user', 'recipe',)
