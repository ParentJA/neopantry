# Django imports.
from django.contrib.auth import get_user_model

# Third-party imports.
import factory
from factory import RelatedFactory, SubFactory, faker, fuzzy
from factory.django import DjangoModelFactory

__author__ = 'Jason Parent'


class UserFactory(DjangoModelFactory):
    username = faker.Faker('email')
    password = faker.Faker('password')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return get_user_model().objects.create_user(**kwargs)

    class Meta:
        model = get_user_model()


class FoodFactory(DjangoModelFactory):
    name = faker.Faker('word')

    class Meta:
        model = 'recipes.Food'


class RecipeFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Recipe {n}')
    description = faker.Faker('paragraph', nb_sentences=1)
    instructions = faker.Faker('paragraph', nb_sentences=3)

    class Meta:
        model = 'recipes.Recipe'


class IngredientFactory(DjangoModelFactory):
    description = faker.Faker('sentence')
    recipe = SubFactory(RecipeFactory)
    food = SubFactory(FoodFactory)
    rank = 0
    is_optional = faker.Faker('boolean')

    class Meta:
        model = 'recipes.Ingredient'


class FoodWithRecipeFactory(FoodFactory):
    ingredient = RelatedFactory(IngredientFactory, 'food')


class FullRecipeFactory(RecipeFactory):
    food = RelatedFactory(IngredientFactory)


class RecipeNoteFactory(DjangoModelFactory):
    note = faker.Faker('sentence')

    class Meta:
        model = 'recipes.RecipeNote'


class RecipeReviewFactory(DjangoModelFactory):
    recipe = SubFactory(RecipeFactory)
    user = SubFactory(UserFactory)
    make_again = faker.Faker('boolean')
    rating = fuzzy.FuzzyInteger(low=1, high=5)
    review = faker.Faker('sentence')

    class Meta:
        model = 'recipes.RecipeReview'


class UserRecipeFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    recipe = SubFactory(RecipeFactory)

    class Meta:
        model = 'recipes.UserRecipe'
