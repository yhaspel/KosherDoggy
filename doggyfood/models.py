from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class DogFood(models.Model):
    title = models.TextField(max_length=200)
    description = models.TextField(max_length=1000)
    photo = models.ImageField(upload_to="uploads/", null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='dogfoods')

    # def get_absolute_url(self):
    #     return reverse("doggyfood:detail", args=(self.pk,))
    def __str__(self):
        return self.title


class Ingredient(models.Model):
    dog_foods = models.ManyToManyField(DogFood, related_name='ingredients', blank=True)
    name = models.TextField(max_length=200)


    def __str__(self):
        return self.name