from django.db import models


class DogFood(models.Model):
    title = models.TextField(max_length=200)
    description = models.TextField(max_length=1000)
    photo = models.ImageField(null=True, blank=True)


class Ingredient(models.Model):
    dog_food = models.ForeignKey(DogFood, related_name='ingredient')
    name = models.TextField(max_length=200)
