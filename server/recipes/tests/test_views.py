import json
from unittest.mock import patch

from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from ..models import Recipe, RecipeNote, RecipeSearchWord, UserRecipe
from ..serializers import RecipeNoteSerializer

PASSWORD = 'pAssW0rd!'


class RecipeViewTest(APITestCase):
    def setUp(self):
        self.user = baker.make('accounts.User', password=PASSWORD)
        self.client = APIClient()
        self.client.login(username=self.user.username, password=PASSWORD)

    def test_user_can_retrieve_recipe(self):
        # Given.
        ingredient = baker.make('recipes.Ingredient')
        recipe = ingredient.recipe

        # When.
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': recipe.pk}))

        # Then.
        self.assertEqual(200, response.status_code)
        self.assertEqual(recipe.id, response.data['id'])
        self.assertEqual(recipe.name, response.data['name'])
        self.assertEqual(recipe.description, response.data['description'])
        self.assertEqual(recipe.instructions, response.data['instructions'])
        self.assertIn(recipe.photo.url, response.data['photo'])
        self.assertEqual(recipe.average_rating, response.data['average_rating'])
        self.assertEqual(recipe.num_reviews, response.data['num_reviews'])
        self.assertEqual(ingredient.description, response.data['ingredients'][0].get('description'))
        self.assertEqual(ingredient.rank, response.data['ingredients'][0].get('rank'))


class RecipeSearchViewTest(APITestCase):
    def setUp(self):
        self.user = baker.make('accounts.User', password=PASSWORD)
        self.client = APIClient()
        self.client.login(username=self.user.username, password=PASSWORD)

    def test_saving_recipe_updates_search_vector(self):
        recipe = baker.make('recipes.Recipe')
        recipe = Recipe.objects.get(id=recipe.id)
        self.assertIsNotNone(recipe.search_vector)

    def test_saving_recipe_updates_recipe_search_words(self):
        recipe = baker.make('recipes.Recipe')
        recipe = Recipe.objects.get(id=recipe.id)
        self.assertGreater(RecipeSearchWord.objects.count(), 0)

    def test_user_can_search_recipes(self):
        # Given.
        recipe1 = baker.make('recipes.Recipe', name='Chicken Pot Pie')
        recipe2 = baker.make('recipes.Recipe', name='Apple Pie')
        baker.make('recipes.Recipe', name='Test', description='This is a test.', _quantity=3)

        # When.
        response = self.client.get(path=reverse('recipes:recipe-search'), data={'page': 1, 'query': 'pies'})

        # Then.
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.data['count'])

        # Get expected recipe IDs.
        exp = [recipe1.pk, recipe2.pk]

        # Get actual recipe IDs.
        act = [result.get('id') for result in response.data['results']]

        self.assertCountEqual(exp, act)

    def test_user_can_list_recipes(self):
        # Given.
        recipes = baker.make('recipes.Recipe', _quantity=10)

        # When.
        response = self.client.get(path=reverse('recipes:recipe-search'), data={'page': 1})

        # Then.
        self.assertEqual(200, response.status_code)
        self.assertEqual(10, response.data['count'])

        # Get expected recipe IDs.
        exp = [recipe.pk for recipe in recipes]

        # Get actual recipe IDs.
        act = [result.get('id') for result in response.data['results']]

        self.assertCountEqual(exp, act)

    def test_user_can_list_recipes_with_pagination(self):
        # Given.
        recipes = baker.make('recipes.Recipe', _quantity=15)

        # When.
        with patch('recipes.pagination.RecipePagination.get_page_size', return_value=10):
            response = self.client.get(path=reverse('recipes:recipe-search'), data={'page': 1})

        # Then.
        self.assertEqual(200, response.status_code)

        # Has 15 total results.
        self.assertEqual(15, response.data['count'])

        # Showing 10 results.
        self.assertEqual(10, len(response.data['results']))

    def test_user_can_list_recipes_with_reviews(self):
        # Given.
        recipe = baker.make('recipes.Recipe')
        recipe_reviews = baker.make('recipes.RecipeReview', recipe=recipe, _quantity=5)

        # When.
        response = self.client.get(reverse('recipes:recipe-search'))

        # Then.
        self.assertEqual(200, response.status_code)
        # self.assertCountEqual(
        #     RecipeListSerializer(Recipe.objects.all(), many=True).data,
        #     response.data
        # )
        #
        # def num_reviews(reviews):
        #     return len(reviews)
        #
        # self.assertEqual(num_reviews(recipe_reviews), response.data[0].get('num_reviews'))


class RecipeNoteTest(APITestCase):
    def setUp(self):
        self.user = baker.make('accounts.User', password=PASSWORD)
        self.client = APIClient()
        self.client.login(username=self.user.username, password=PASSWORD)

    def test_user_can_list_recipe_notes(self):
        # Given.
        recipe = baker.make('recipes.Recipe')
        baker.make('recipes.RecipeNote', recipe=recipe, user=self.user)

        # When.
        response = self.client.get(reverse('recipes:recipe-note-list'), data={'recipe': recipe.pk})

        # Then.
        self.assertEqual(200, response.status_code)
        # self.assertEqual(RecipeNoteSerializer(RecipeNote.objects.all(), many=True).data, response.data)

    def test_user_can_only_list_own_notes(self):
        # Given.
        recipe = baker.make('recipes.Recipe')
        other_user = baker.make('accounts.User')
        baker.make('recipes.RecipeNote', recipe=recipe, user=other_user)

        # When.
        response = self.client.get(reverse('recipes:recipe-note-list'), data={'recipe': recipe.pk})

        # Then.
        self.assertEqual(200, response.status_code)
        self.assertListEqual([], response.data)

    def test_user_can_create_recipe_note(self):
        # Given.
        recipe = baker.make('recipes.Recipe')

        # When.
        response = self.client.post(reverse('recipes:recipe-note-list'), data={
            'note': 'This is a note.',
            'recipe': recipe.pk,
            'user': self.user.pk,
        })

        # Then.
        self.assertEqual(201, response.status_code)
        # self.assertEqual(RecipeNoteSerializer(RecipeNote.objects.last()).data, response.data)

    def test_user_can_retrieve_recipe_note(self):
        # Given.
        recipe = baker.make('recipes.Recipe')
        recipe_note = baker.make('recipes.RecipeNote', recipe=recipe, user=self.user)

        # When.
        response = self.client.get(reverse('recipes:recipe-note-detail', kwargs={'pk': recipe_note.pk}))

        # Then.
        self.assertEqual(200, response.status_code)
        # self.assertEqual(RecipeNoteSerializer(RecipeNote.objects.get(pk=recipe_note.pk)).data, response.data)

    def test_user_can_only_retrieve_own_note(self):
        # Given.
        recipe = baker.make('recipes.Recipe')
        other_user = baker.make('accounts.User')
        recipe_note = baker.make('recipes.RecipeNote', recipe=recipe, user=other_user)

        # When.
        response = self.client.get(reverse('recipes:recipe-note-detail', kwargs={'pk': recipe_note.pk}))

        # Then.
        self.assertEqual(404, response.status_code)

    def test_user_can_update_recipe_note(self):
        # Given.
        recipe = baker.make('recipes.Recipe')
        recipe_note = baker.make('recipes.RecipeNote', recipe=recipe, user=self.user)

        # When.
        response = self.client.put(reverse('recipes:recipe-note-detail', kwargs={'pk': recipe_note.pk}), data={
            **RecipeNoteSerializer(recipe_note).data,
            'note': 'A new note.',
            'user': self.user.pk,
        })

        # Then.
        self.assertEqual(200, response.status_code)
        # self.assertEqual(RecipeNoteSerializer(RecipeNote.objects.get(pk=recipe_note.pk)).data, response.data)

    def test_user_can_only_update_own_note(self):
        # Given.
        recipe = baker.make('recipes.Recipe')
        other_user = baker.make('accounts.User')
        recipe_note = baker.make('recipes.RecipeNote', recipe=recipe, user=other_user)

        # When.
        response = self.client.put(reverse('recipes:recipe-note-detail', kwargs={'pk': recipe_note.pk}), data={
            **RecipeNoteSerializer(recipe_note).data,
            'note': 'A new note.',
            'user': other_user.pk,
        })

        # Then.
        self.assertEqual(403, response.status_code)

    def test_user_can_destroy_recipe_note(self):
        # Given.
        recipe = baker.make('recipes.Recipe')
        recipe_note = baker.make('recipes.RecipeNote', recipe=recipe, user=self.user)

        # When.
        response = self.client.delete(reverse('recipes:recipe-note-detail', kwargs={'pk': recipe_note.pk}))

        # Then.
        self.assertEqual(204, response.status_code)
        # self.assertIsNone(response.data)
        self.assertFalse(RecipeNote.objects.filter(pk=recipe_note.pk).exists())

    def test_user_can_only_destroy_own_note(self):
        # Given.
        recipe = baker.make('recipes.Recipe')
        other_user = baker.make('accounts.User')
        recipe_note = baker.make('recipes.RecipeNote', recipe=recipe, user=other_user)

        # When.
        response = self.client.delete(reverse('recipes:recipe-note-detail', kwargs={'pk': recipe_note.pk}))

        # Then.
        self.assertEqual(404, response.status_code)
        self.assertTrue(RecipeNote.objects.filter(pk=recipe_note.pk).exists())


class RecipeReviewTest(APITestCase):
    def setUp(self):
        self.user1 = baker.make('accounts.User', password=PASSWORD)
        self.user2 = baker.make('accounts.User', password=PASSWORD)
        self.client = APIClient()
        self.client.login(username=self.user1.username, password=PASSWORD)

    def test_user_can_create_recipe_review(self):
        # Given.
        recipe = baker.make('recipes.Recipe', total_make_again=4, total_ratings=20, num_reviews=4)
        review = baker.prepare('recipes.RecipeReview', recipe=recipe, user=self.user1, make_again=True, rating=5)

        # And.
        self.assertEqual(5.0, recipe.average_rating)

        # When.
        response = self.client.post(reverse('recipes:recipe-review'), data={
            'recipe': review.recipe.pk,
            'user': review.user.pk,
            'make_again': review.make_again,
            'rating': review.rating,
            'review': review.review,
        })

        # Then.
        self.assertEqual(201, response.status_code)
        self.assertEqual(review.recipe.pk, response.data['recipe'])
        self.assertEqual(review.user.pk, response.data['user'])
        self.assertEqual(review.make_again, response.data['make_again'])
        self.assertEqual(review.rating, response.data['rating'])
        self.assertEqual(review.review, response.data['review'])
        self.assertEqual(review.user.username, response.data['username'])

        # And.
        recipe = Recipe.objects.get(pk=recipe.pk)
        self.assertEqual(100, recipe.average_make_again)
        self.assertEqual(5, recipe.average_rating)
        self.assertEqual(5, recipe.num_reviews)

    def test_updating_review_updates_recipe(self):
        # Given.
        recipe = baker.make('recipes.Recipe', total_make_again=1, total_ratings=5, num_reviews=1)
        review = baker.make('recipes.RecipeReview', recipe=recipe, user=self.user1, make_again=True, rating=5)

        # And.
        self.assertEqual(100, recipe.average_make_again)
        self.assertEqual(5.0, recipe.average_rating)

        # When.
        response = self.client.put(reverse('recipes:recipe-review-by-id', kwargs={'pk': review.pk}), data={
            'recipe': review.recipe.pk,
            'user': review.user.pk,
            'make_again': False,
            'rating': 3,
            'review': review.review,
        })

        # Then.
        self.assertEqual(200, response.status_code)
        self.assertEqual(review.recipe.pk, response.data['recipe'])
        self.assertEqual(review.user.pk, response.data['user'])
        self.assertEqual(False, response.data['make_again'])
        self.assertEqual(3, response.data['rating'])
        self.assertEqual(review.review, response.data['review'])

        # And.
        recipe = Recipe.objects.get(pk=recipe.pk)
        self.assertEqual(0, recipe.average_make_again)
        self.assertEqual(3, recipe.average_rating)
        self.assertEqual(1, recipe.num_reviews)

    def test_destroying_review_updates_recipe(self):
        # Given.
        recipe = baker.make('recipes.Recipe', total_make_again=1, total_ratings=5, num_reviews=1)
        review = baker.make('recipes.RecipeReview', recipe=recipe, user=self.user1, make_again=True, rating=5)

        # And.
        self.assertEqual(100, recipe.average_make_again)
        self.assertEqual(5.0, recipe.average_rating)

        # When.
        response = self.client.delete(reverse('recipes:recipe-review-by-id', kwargs={'pk': review.pk}))

        # Then.
        self.assertEqual(204, response.status_code)

        # And.
        recipe = Recipe.objects.get(pk=recipe.pk)
        self.assertEqual(0, recipe.average_make_again)
        self.assertEqual(0, recipe.average_rating)
        self.assertEqual(0, recipe.num_reviews)

    def test_user_can_only_create_recipe_review_for_self(self):
        # Given.
        recipe = baker.make('recipes.Recipe')
        review = baker.prepare('recipes.RecipeReview', recipe=recipe, user=self.user2)

        # When.
        response = self.client.post(reverse('recipes:recipe-review'), data={
            'recipe': review.recipe.pk,
            'user': review.user.pk,
            'make_again': review.make_again,
            'rating': review.rating,
            'review': review.review,
        })

        # Then.
        self.assertEqual(403, response.status_code)

    def test_user_can_only_create_one_review_per_recipe(self):
        # Given.
        recipe = baker.make('recipes.Recipe')
        review = baker.make('recipes.RecipeReview', recipe=recipe, user=self.user1)

        # When.
        response = self.client.post(reverse('recipes:recipe-review'), data={
            'recipe': review.recipe.pk,
            'user': review.user.pk,
            'make_again': review.make_again,
            'rating': review.rating,
            'review': review.review,
        })

        # Then.
        self.assertEqual(400, response.status_code)

    def test_user_can_get_reviews_by_recipe(self):
        # Given.
        recipe1 = baker.make('recipes.Recipe')
        review1 = baker.make('recipes.RecipeReview', recipe=recipe1, user=self.user1)
        recipe2 = baker.make('recipes.Recipe')
        review2 = baker.make('recipes.RecipeReview', recipe=recipe2, user=self.user2)

        # When.
        response = self.client.get(reverse('recipes:recipe-review'), data={
            'recipe': recipe1.pk
        })

        # Then.
        self.assertEqual(200, response.status_code)
        self.assertCountEqual([recipe1.pk], [data.get('recipe') for data in response.data])

    def test_user_can_get_reviews_by_user(self):
        # Given.
        recipe1 = baker.make('recipes.Recipe')
        review1 = baker.make('recipes.RecipeReview', recipe=recipe1, user=self.user1)
        recipe2 = baker.make('recipes.Recipe')
        review2 = baker.make('recipes.RecipeReview', recipe=recipe2, user=self.user2)

        # When.
        response = self.client.get(reverse('recipes:recipe-review'), data={
            'user': self.user1.pk
        })

        # Then.
        self.assertEqual(200, response.status_code)
        self.assertCountEqual([self.user1.pk], [data.get('user') for data in response.data])


class UserRecipeTest(APITestCase):
    def setUp(self):
        self.user1 = baker.make('accounts.User', password=PASSWORD)
        self.user2 = baker.make('accounts.User', password=PASSWORD)
        self.client = APIClient()
        self.client.login(username=self.user1.username, password=PASSWORD)

    def test_user_can_get_saved_recipes(self):
        # Given.
        baker.make('recipes.UserRecipe', user=self.user1, _quantity=3)
        baker.make('recipes.UserRecipe', user=self.user2, _quantity=2)

        # When.
        response = self.client.get(reverse('recipes:user-recipe-search', kwargs={'user_pk': self.user1.pk}))

        # Then.
        self.assertEqual(200, response.status_code)

        # Get 'user' and 'recipe' values from database records.
        exp = UserRecipe.objects.filter(user=self.user1).values_list('user', 'recipe')

        # Get 'user' and 'recipe' values from response data.
        act = [(result['user'], result['recipe'].get('id')) for result in response.data['results']]

        self.assertCountEqual(exp, act)

    def test_user_cannot_get_other_users_saved_recipes(self):
        # Given.
        baker.make('recipes.UserRecipe', user=self.user2, _quantity=3)

        # When.
        # NOTE: Logged in as 'user1'.
        response = self.client.get(reverse('recipes:user-recipe-search', kwargs={'user_pk': self.user2.pk}))

        # Then.
        self.assertEqual(403, response.status_code)

    def test_user_can_save_recipes(self):
        # Given.
        recipe = baker.make('recipes.Recipe')

        # Get 'recipe' count from database.
        self.assertEqual(UserRecipe.objects.filter(user=self.user1).count(), 0)

        # When.
        response = self.client.post(reverse('recipes:user-recipe-search', kwargs={
            'user_pk': self.user1.pk
        }), data=json.dumps({
            'user': self.user1.pk,
            'recipe': {
                'id': recipe.pk,
                'name': recipe.name,
            },
        }), content_type='application/json')

        # Then.
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.user1.pk, response.data['user'])
        self.assertEqual(recipe.pk, response.data['recipe'].get('id'))

        # Get 'recipe' count from database.
        self.assertEqual(UserRecipe.objects.filter(user=self.user1).count(), 1)

    def test_user_cannot_save_recipe_more_than_once(self):
        # Given.
        user_recipe = baker.make('recipes.UserRecipe', user=self.user1)

        # When.
        response = self.client.post(reverse('recipes:user-recipe-search', kwargs={'user_pk': self.user1.pk}), data={
            'recipe': user_recipe.recipe.pk
        })

        # Then.
        self.assertEqual(400, response.status_code)

    def test_user_can_delete_recipes(self):
        # Given.
        user_recipe = baker.make('recipes.UserRecipe', user=self.user1)

        # When.
        response = self.client.delete(reverse('recipes:user-recipe', kwargs={
            'user_pk': self.user1.pk, 'recipe_pk': user_recipe.recipe.pk
        }))

        # Then.
        self.assertEqual(204, response.status_code)

    def test_user_cannot_delete_other_users_recipes(self):
        # Given.
        user_recipe = baker.make('recipes.UserRecipe', user=self.user2)

        # When.
        response = self.client.delete(reverse('recipes:user-recipe', kwargs={
            'user_pk': user_recipe.user.pk, 'recipe_pk': user_recipe.recipe.pk
        }))

        # Then.
        self.assertEqual(403, response.status_code)
