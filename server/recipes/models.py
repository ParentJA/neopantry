import decimal
import math

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVectorField, TrigramSimilarity
from django.db import models
from django.db.models import F, Q, QuerySet
from django.utils.functional import cached_property


class RecipeQuerySet(QuerySet):
    def allergens(self, *, allergens):
        """
        Returns a list of recipes that don't have the specified allergens.
        :param Tuple[str] allergens: a tuple of allergen names
        :return: recipes
        """

        sql = """
            WITH food_allergens AS (
                SELECT food.id AS food_id
                  FROM recipes_food food
                  LEFT JOIN recipes_food_allergens food_allergen
                    ON food.id = food_allergen.food_id
                  LEFT JOIN recipes_allergen allergen
                    ON food_allergen.allergen_id = allergen.id
                 WHERE allergen.name IN %s
            ),
            recipes_with_allergens AS (
                SELECT DISTINCT recipe.id
                  FROM recipes_recipe recipe
                  LEFT JOIN recipes_ingredient ingredient
                    ON recipe.id = ingredient.recipe_id
                  LEFT JOIN recipes_food food
                    ON ingredient.food_id = food.id
                 WHERE food.id IN (
                     SELECT DISTINCT food_id 
                       FROM food_allergens
                 ) 
            )
            SELECT *
              FROM recipes_recipe recipe
             WHERE recipe.id NOT IN (
                 SELECT id
                   FROM recipes_with_allergens
             );
        """
        return self.raw(raw_query=sql, params=[allergens])

    def search(self, query):
        search_query = SearchQuery(query, search_type='plain')
        return self.annotate(
            search_rank=SearchRank(F('search_vector'), search_query),
        ).filter(
            search_vector=search_query,
        ).order_by(
            '-search_rank', 'id'
        )


class RecipeManager(models.Manager.from_queryset(RecipeQuerySet)):
    use_in_migrations = True


class Recipe(models.Model):
    """A preparation of foods."""

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    ingredients_text = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    foods = models.ManyToManyField('recipes.Food', through='recipes.Ingredient', through_fields=('recipe', 'food'))
    photo = models.ImageField(upload_to='photos', default='photos/no-image.jpg', blank=True, null=True)
    total_make_again = models.IntegerField(default=0, editable=False)
    total_ratings = models.IntegerField(default=0, editable=False)
    num_reviews = models.IntegerField(default=0, editable=False)
    search_vector = SearchVectorField(null=True, blank=True)

    objects = RecipeManager()

    @staticmethod
    def autocomplete_search_fields():
        return 'name__icontains',

    @property
    def average_make_again(self):
        if self.num_reviews > 0:
            return math.ceil(100 * self.total_make_again / self.num_reviews)
        return 0

    @property
    def average_rating(self):
        if self.num_reviews > 0:
            return math.ceil(self.total_ratings / self.num_reviews)
        return 0

    class Meta:
        default_related_name = 'recipes'
        indexes = (
            GinIndex(fields=['search_vector'], name='recipe_search_vector_index'),
        )
        ordering = ('name',)

    def __str__(self):
        return self.name
    

class RecipeSearchWordQuerySet(models.query.QuerySet):
    def search(self, query):
        return self.annotate(
            similarity=TrigramSimilarity('word', query)
        ).filter(similarity__gte=0.3).order_by('-similarity')


class RecipeSearchWord(models.Model):
    word = models.CharField(max_length=255, unique=True)

    objects = RecipeSearchWordQuerySet.as_manager()

    def __str__(self):
        return self.word


class Ingredient(models.Model):
    """A food that is prepared and used in a recipe in measured amounts."""

    description = models.CharField(max_length=255)
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    food = models.ForeignKey('recipes.Food', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=3, max_digits=6, null=True, blank=True)
    measurement = models.ForeignKey('recipes.Measurement', null=True, blank=True, on_delete=models.SET_NULL)
    rank = models.IntegerField(default=0)
    is_optional = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'ingredients'
        unique_together = ('recipe', 'food', 'rank',)

    def __str__(self):
        return self.description


class Food(models.Model):
    """An edible item."""

    name = models.CharField(max_length=255, unique=True)
    allergens = models.ManyToManyField('recipes.Allergen', blank=True)

    @staticmethod
    def autocomplete_search_fields():
        return 'name__icontains',

    class Meta:
        default_related_name = 'foods'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    """A food item for sale."""

    food = models.ForeignKey('recipes.Food', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    amount = models.DecimalField(decimal_places=3, max_digits=6)
    measurement = models.ForeignKey('recipes.Measurement', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'products'

    @cached_property
    def price_per_unit(self):
        return self.price / self.amount


class Measurement(models.Model):
    """A unit of measure."""

    QUANTITY = 'QUANTITY'
    WEIGHT = 'WEIGHT'
    VOLUME = 'VOLUME'

    MEASUREMENT_TYPES = (
        (QUANTITY, QUANTITY),
        (WEIGHT, WEIGHT),
        (VOLUME, VOLUME)
    )

    TEASPOON = 'TEASPOON'
    TABLESPOON = 'TABLESPOON'
    CUP = 'CUP'
    PINT = 'PINT'
    QUART = 'QUART'
    GALLON = 'GALLON'
    OUNCE = 'OUNCE'
    POUND = 'POUND'

    MEASUREMENT_UNITS = (
        (TEASPOON, TEASPOON),
        (TABLESPOON, TABLESPOON),
        (CUP, CUP),
        (PINT, PINT),
        (QUART, QUART),
        (GALLON, GALLON),
        (OUNCE, OUNCE),
        (POUND, POUND)
    )

    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255, null=True, blank=True)
    measurement_type = models.CharField(max_length=255, choices=MEASUREMENT_TYPES)
    measurement_unit = models.CharField(max_length=255, choices=MEASUREMENT_UNITS)

    @staticmethod
    def autocomplete_search_fields():
        return 'name__icontains', 'abbreviation__icontains',

    def __str__(self):
        return self.name


class MeasurementConversion(models.Model):
    """A table mapping quantity, weight, and volume measurements to a specific food."""

    WEIGHT_CONVERSION = {
        Measurement.POUND: decimal.Decimal(16.0),
        Measurement.OUNCE: decimal.Decimal(1.0)
    }

    VOLUME_CONVERSION = {
        Measurement.GALLON: decimal.Decimal(768.0),
        Measurement.QUART: decimal.Decimal(192.0),
        Measurement.PINT: decimal.Decimal(96.0),
        Measurement.CUP: decimal.Decimal(48.0),
        Measurement.TABLESPOON: decimal.Decimal(3.0),
        Measurement.TEASPOON: decimal.Decimal(1.0)
    }

    CONVERSION_TABLE = {
        Measurement.WEIGHT: WEIGHT_CONVERSION,
        Measurement.VOLUME: VOLUME_CONVERSION
    }

    food = models.ForeignKey('recipes.Food', on_delete=models.CASCADE)
    weight = models.DecimalField(decimal_places=3, max_digits=6)
    weight_measurement = models.ForeignKey(
        'recipes.Measurement', related_name='weight_measurement_conversions', on_delete=models.CASCADE
    )
    volume = models.DecimalField(decimal_places=3, max_digits=6)
    volume_measurement = models.ForeignKey(
        'recipes.Measurement', related_name='volume_measurement_conversions', on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = 'measurement_conversions'

    def convert_measurement(self, *, amount, measurement1, measurement2):
        """
        Converts the specified amount from one measurement to another, using a conversion table.
        :param amount: the amount of a Food
        :param Measurement measurement1: the Measurement converted from
        :param Measurement measurement2: the Measurement converted to
        :return: the amount converted to the specified measurement
        """

        # If the measurements have the same units, return the amount. No conversion necessary.
        if measurement1.measurement_unit == measurement2.measurement_unit:
            return decimal.Decimal(amount)

        # If the measurements are the same type, convert using the table and return the amount.
        if measurement1.measurement_type == measurement2.measurement_type:
            conversion_table = self.CONVERSION_TABLE[measurement1.measurement_type]
            return (
                decimal.Decimal(amount) *
                conversion_table[measurement1.measurement_unit] /
                conversion_table[measurement2.measurement_unit]
            )

        else:
            # Convert measurement 1 unit to measurement conversion unit.
            amount = self.convert_measurement(
                amount=amount,
                measurement1=measurement1,
                measurement2=self.get_measurement_by_type(measurement_type=measurement1.measurement_type)
            )

            # Convert measurement 1 type to measurement 2 type.
            amount *= (self.get_amount_by_type(measurement_type=measurement2.measurement_type) /
                       self.get_amount_by_type(measurement_type=measurement1.measurement_type))

            # Convert amount back to measurement 2 unit.
            return self.convert_measurement(
                amount=amount,
                measurement1=self.get_measurement_by_type(measurement_type=measurement2.measurement_type),
                measurement2=measurement2
            )

    def get_measurement_by_type(self, *, measurement_type):
        """Returns the Measurement by the type."""

        return {
            Measurement.WEIGHT: self.weight_measurement,
            Measurement.VOLUME: self.volume_measurement
        }[measurement_type]

    def get_amount_by_type(self, *, measurement_type):
        """Returns the amount by the type."""

        return {
            Measurement.WEIGHT: decimal.Decimal(self.weight),
            Measurement.VOLUME: decimal.Decimal(self.volume)
        }[measurement_type]


class Allergen(models.Model):
    """A food allergen."""

    name = models.CharField(max_length=255)

    @staticmethod
    def autocomplete_search_fields():
        return 'name__icontains',

    def __str__(self):
        return self.name


class RecipeNote(models.Model):
    """A user's note on a recipe."""

    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.TextField()
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name = 'notes'
        ordering = ('-updated_ts',)

    def __str__(self):
        return f'{self.recipe}: {self.user}'


class RecipeReview(models.Model):
    """A user's review of a recipe."""

    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    make_again = models.BooleanField()
    rating = models.IntegerField()
    review = models.TextField(null=True, blank=True)

    class Meta:
        default_related_name = 'reviews'
        unique_together = ('recipe', 'user',)

    def __str__(self):
        return f'{self.recipe}: {self.user}'


class UserRecipe(models.Model):
    """A recipe saved by a user."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'user_recipes'
        unique_together = ('user', 'recipe',)

    def __str__(self):
        return f'{self.user}: {self.recipe}'
