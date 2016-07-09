import csv
import os

from doggyfood.models import Brand
from doggyfood.models import Category
from doggyfood.models import DogFood
from doggyfood.models import Ingredient
from doggyfood.models import NutritionalFact
from doggyfood.models import IngredientComposition
from doggyfood.models import NutritionalComposition


paths = [
    os.path.join('', 'KosherDoggyData', 'brands.csv'),
    os.path.join('', 'KosherDoggyData', 'categories.csv'),
    os.path.join('', 'KosherDoggyData', 'dogfoods.csv'),
    os.path.join('', 'KosherDoggyData', 'ingredients.csv'),
    os.path.join('', 'KosherDoggyData', 'nutritionalfacts.csv'),
    os.path.join('', 'KosherDoggyData', 'ingredientcomp.csv'),
    os.path.join('', 'KosherDoggyData', 'nutritionalcomp.csv'),
]


def populate_brands():
    with open(paths[0]) as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = Brand.objects.get_or_create(
                name=row[0],
                description=row[1],
            )
            # item = Brand(**row)
            # item.save()


def populate_categories():
    with open(paths[1]) as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = Category.objects.get_or_create(
                name=row[0],
                type=row[1],
                description=row[2],
            )


def populate_dogfoods():
    with open(paths[2]) as f:
        reader = csv.reader(f)
        for row in reader:
            brand, _ = Brand.objects.get_or_create(name=row[1])
            _, created = DogFood.objects.get_or_create(
                title=row[0],
                brand=brand,
                description=row[2],
                photo=row[3],
            )

            df = DogFood.objects.get(title=row[0])

            for cat in row[4].split(';'):
                category, _ = Category.objects.get_or_create(name=cat)
                df.category.add(category)

            for ing in row[5].split(';'):
                ingredient, _ = Ingredient.objects.get_or_create(name=ing)
                df.ingredients.add(ingredient)

            df.save()


def populate_ingredients():
    with open(paths[3]) as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = Ingredient.objects.get_or_create(
                name=row[0],
                description=row[1],
            )


def populate_nutritional_facts():
    with open(paths[4]) as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = NutritionalFact.objects.get_or_create(
                name=row[0],
                description=row[1],
            )


def populate_ingredient_composition():
    with open(paths[5]) as f:
        reader = csv.reader(f)
        for row in reader:
            ingredient, _ = Ingredient.objects.get_or_create(name=row[0])
            dog_food, _ = DogFood.objects.get_or_create(title=row[1])
            _, created = IngredientComposition.objects.get_or_create(
                ingredient=ingredient,
                dog_food=dog_food,
                composition=row[2]
            )


def populate_nutritional_composition():
    with open(paths[6]) as f:
        reader = csv.reader(f)
        for row in reader:
            nutritional_fact, _ = NutritionalFact.objects.get_or_create(name=row[0])
            dog_food, _ = DogFood.objects.get_or_create(title=row[1])
            _, created = NutritionalComposition.objects.get_or_create(
                nutritional_fact=nutritional_fact,
                dog_food=dog_food,
                composition=row[2]
            )


def populate_all():
    populate_brands()
    populate_categories()
    populate_ingredients()
    populate_dogfoods()
    populate_nutritional_facts()
    populate_ingredient_composition()
    populate_nutritional_composition()


print("Done")
