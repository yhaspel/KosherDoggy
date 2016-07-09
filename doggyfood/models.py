import os

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


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
