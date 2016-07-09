from django.contrib import admin
from . import models

admin.site.register(models.DogFood)
admin.site.register(models.Ingredient)
admin.site.register(models.Category)
admin.site.register(models.NutritionalFact)
admin.site.register(models.Brand)
admin.site.register(models.IngredientComposition)
admin.site.register(models.NutritionalComposition)
