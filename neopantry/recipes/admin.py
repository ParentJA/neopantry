# Django imports.
from django import forms
from django.contrib import admin
from django.template.defaultfilters import striptags, truncatechars_html

# Third-party imports.
from tinymce.widgets import TinyMCE

# Local imports.
from .models import Allergen, Food, Measurement, Recipe, RecipeNote, RecipeReview, RecipeSearchWord, UserRecipe

__author__ = 'Jason Parent'


class IngredientInline(admin.TabularInline):
    model = Recipe.foods.through
    extra = 1

    # Handle fields.
    fields = ('description', 'food', 'amount', 'measurement', 'rank', 'is_optional',)
    raw_id_fields = ('food', 'measurement',)
    autocomplete_lookup_fields = {
        'fk': ('food', 'measurement',)
    }


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    change_form_template = 'recipes/admin/change_form.html'
    fields = ('name', 'description', 'instructions', 'photo',)
    readonly_fields = ('short_description', 'average_make_again', 'average_rating', 'num_reviews', 'search_vector',)
    list_display = ('name', 'short_description', 'photo', 'average_make_again', 'average_rating', 'num_reviews',)
    inlines = (IngredientInline,)

    def short_description(self, instance):
        return striptags(truncatechars_html(instance.description, 255))

    short_description.short_description = 'Short description'


@admin.register(RecipeSearchWord)
class RecipeSearchWordAdmin(admin.ModelAdmin):
    fields = ('id', 'recipe', 'word',)
    list_display = ('id', 'recipe', 'word',)
    list_filter = ('recipe',)
    list_select_related = ('recipe',)
    raw_id_fields = ('recipe',)
    readonly_fields = ('id',)


class AllergenInline(admin.TabularInline):
    model = Food.allergens.through
    extra = 1

    # Handle fields.
    fields = ('allergen',)
    raw_id_fields = ('allergen',)
    autocomplete_lookup_fields = {
        'fk': ('allergen',)
    }


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
    inlines = (AllergenInline,)


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    fields = ('name', 'abbreviation', 'measurement_type', 'measurement_unit',)
    list_display = ('name', 'abbreviation', 'measurement_type', 'measurement_unit',)


@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


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
    autocomplete_lookup_fields = {
        'fk': ('recipe', 'user',)
    }


@admin.register(UserRecipe)
class UserRecipeAdmin(admin.ModelAdmin):
    fields = ('user', 'recipe',)
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    list_select_related = ('user', 'recipe',)
    raw_id_fields = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    autocomplete_lookup_fields = {
        'fk': ('user', 'recipe',)
    }
