import os

from django.contrib import messages
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from star_ratings.models import Rating


class Category(models.Model):
    LIFE_STAGE = 'LS'
    SPECIAL_NUTRITION = 'SN'
    DOG_SIZE = 'DS'
    QUALITY = 'QL'
    OTHER = 'OT'

    TYPES = [
        (LIFE_STAGE, 'Life Stage'),
        (SPECIAL_NUTRITION, 'Special Nutrition'),
        (DOG_SIZE, 'Dog Size'),
        (QUALITY, 'Quality'),
        (OTHER, 'Other'),
    ]

    name = models.CharField(max_length=200)
    type = models.CharField(
        max_length=2,
        choices=TYPES,
        default=OTHER,
    )
    description = models.TextField(max_length=1000, blank=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def type_verbose(self):
        return dict(Category.TYPES)[self.type]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.TextField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.TextField(max_length=200)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class DogFood(models.Model):
    title = models.TextField(max_length=200)
    brand = models.ForeignKey(Brand, related_name='dogfoods')
    description = models.TextField(max_length=1000, blank=True)
    photo = models.ImageField(upload_to="uploads/", default=os.path.join('', 'misc', 'no-image.jpg'), null=True,
                              blank=True)
    category = models.ManyToManyField(Category, related_name='dogfoods')
    ingredients = models.ManyToManyField(Ingredient, related_name='dogfoods')

    DRY = 'DR'
    RAW = 'RW'
    CANNED = 'CN'
    FRESH = 'FR'
    OTHER = 'OT'
    FOOD_TYPES = [
        (DRY, 'Dry Food'),
        (RAW, 'Raw Food'),
        (CANNED, 'Canned Food'),
        (FRESH, 'Fresh Food'),
        (OTHER, 'Other Food'),
    ]

    food_type = models.CharField(
        max_length=2,
        choices=FOOD_TYPES,
        default=DRY,
    )

    ratings = GenericRelation(Rating, related_query_name='dogfoods')

    def get_rating_avg(self):
        return self.ratings

    def get_ingredient_composition(self, as_dict=False):
        ingredients = self.ingredients.all()
        ing_comps = IngredientComposition.objects.all()
        ing_with_comp = {}

        for ing in ingredients:
            ing_with_comp[ing.name] = ''

        for iwc in ing_with_comp:
            for ing_comp in ing_comps:
                if iwc == ing_comp.ingredient.name and self == ing_comp.dog_food:
                    ing_with_comp[iwc] = ing_comp.composition
        iwc_list = []
        for iwc in ing_with_comp:
            ing_str = '{}'.format(iwc)
            if ing_with_comp[iwc] != '':
                ing_str += ': {}'.format(ing_with_comp[iwc])
            iwc_list.append(ing_str)
        if as_dict:
            return ing_with_comp
        else:
            return iwc_list

    def get_nutritional_composition(self, as_dict=False):
        nutritional_facts = NutritionalFact.objects.all()
        nut_comps = NutritionalComposition.objects.all()
        nut_with_comp = {}

        for nut in nutritional_facts:
             nut_with_comp[nut.name] = ''

        for nwc in nut_with_comp:
            for nut_comp in nut_comps:
                if nwc == nut_comp.nutritional_fact.name and self == nut_comp.dog_food:
                    nut_with_comp[nwc] = nut_comp.composition
        nwc_list = []
        for nwc in nut_with_comp:
            nut_str = ''
            if nut_with_comp[nwc] != '':
                nut_str += '{}: {}%'.format(nwc, nut_with_comp[nwc])
                nwc_list.append(nut_str)
        if as_dict:
            return nut_with_comp
        else:
            return nwc_list

    def get_ing_comp(self):
        return self.ingredients

    # def get_absolute_url(self):
    #     return reverse("doggyfood:detail", args=(self.pk,))
    def __str__(self):
        return self.title


class IngredientComposition(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='ingredient_composition')
    dog_food = models.ForeignKey(DogFood, related_name='ingredient_composition')
    composition = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('ingredient', 'dog_food')

    def __str__(self):
        return self.dog_food.title + '>' + self.ingredient.name + '=' + str(self.composition)


class NutritionalFact(models.Model):
    name = models.TextField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class NutritionalComposition(models.Model):
    nutritional_fact = models.ForeignKey(NutritionalFact, related_name='nutritional_composition')
    dog_food = models.ForeignKey(DogFood, related_name='nutritional_composition')
    composition = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('nutritional_fact', 'dog_food')

    def __str__(self):
        return self.dog_food.title + '>' + self.nutritional_fact.name + '=' + str(self.composition)
