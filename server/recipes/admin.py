from django import forms
from django.contrib import admin
from django.template.defaultfilters import striptags, truncatechars_html

from tinymce.widgets import TinyMCE

from .models import Allergen, Food, Measurement, Recipe, RecipeNote, RecipeReview, RecipeSearchWord, UserRecipe


class IngredientInline(admin.TabularInline):
    model = Recipe.foods.through
    extra = 1

    # Handle fields.
    fields = ('description', 'food', 'amount', 'measurement', 'rank', 'is_optional',)
    raw_id_fields = ('food', 'measurement',)
    autocomplete_fields = ('food', 'measurement',)


class RecipeForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE())
    ingredients_text = forms.CharField(widget=TinyMCE())
    instructions = forms.CharField(widget=TinyMCE())

    class Meta:
        fields = ('description', 'ingredients_text', 'instructions',)
        model = Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = (
        'id', 'name', 'description', 'ingredients_text', 'instructions', 'photo', 'total_make_again', 'average_make_again',
        'total_ratings', 'average_rating', 'num_reviews', 'search_vector',
    )
    form = RecipeForm
    readonly_fields = (
        'id', 'short_description', 'total_make_again', 'average_make_again', 'total_ratings', 'average_rating',
        'num_reviews', 'search_vector',
    )
    list_display = ('name', 'short_description', 'photo', 'average_make_again', 'average_rating', 'num_reviews',)
    search_fields = ('name',)
    inlines = (IngredientInline,)

    def short_description(self, instance):
        return striptags(truncatechars_html(instance.description, 255))

    short_description.short_description = 'Short description'


@admin.register(RecipeSearchWord)
class RecipeSearchWordAdmin(admin.ModelAdmin):
    fields = ('word',)
    list_display = ('word',)
    ordering = ('word',)


class AllergenInline(admin.TabularInline):
    model = Food.allergens.through
    extra = 1

    # Handle fields.
    fields = ('allergen',)
    raw_id_fields = ('allergen',)
    autocomplete_fields = ('allergen',)


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
    search_fields = ('name',)
    inlines = (AllergenInline,)


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    fields = ('name', 'abbreviation', 'measurement_type', 'measurement_unit',)
    list_display = ('name', 'abbreviation', 'measurement_type', 'measurement_unit',)
    search_fields = ('name',)


@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
    search_fields = ('name',)


class RecipeNoteForm(forms.ModelForm):
    note = forms.CharField(widget=TinyMCE())

    class Meta:
        fields = ('recipe', 'user', 'note',)
        model = RecipeNote


@admin.register(RecipeNote)
class RecipeNoteAdmin(admin.ModelAdmin):
    fields = ('recipe', 'user', 'note', 'created_ts', 'updated_ts',)
    form = RecipeNoteForm
    list_display = ('recipe', 'user', 'note',)
    list_filter = ('recipe', 'user',)
    list_select_related = ('recipe', 'user',)
    raw_id_fields = ('recipe', 'user',)
    readonly_fields = ('created_ts', 'updated_ts',)
    search_fields = ('recipe', 'user',)


@admin.register(RecipeReview)
class RecipeReviewAdmin(admin.ModelAdmin):
    fields = ('recipe', 'user', 'make_again', 'rating', 'review',)
    list_display = ('recipe', 'user', 'make_again', 'rating',)
    list_filter = ('recipe', 'user',)
    list_select_related = ('recipe', 'user',)
    raw_id_fields = ('recipe', 'user',)
    search_fields = ('recipe', 'user',)
    autocomplete_fields = ('recipe', 'user',)


@admin.register(UserRecipe)
class UserRecipeAdmin(admin.ModelAdmin):
    fields = ('user', 'recipe',)
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    list_select_related = ('user', 'recipe',)
    raw_id_fields = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    autocomplete_fields = ('user', 'recipe',)
