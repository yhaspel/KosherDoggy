import operator
from functools import reduce

import re
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.encoding import escape_uri_path
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _
from authentication.models import LoggedInMixin, redirect_not_usr
from . import models


class ListFoodsView(LoggedInMixin, ListView):
    model = models.DogFood
    paginate_by = 12
    page_title = _("Home")
    search_text = ''
    exclude_text = ''
    checked_list = []

    def search(self):
        return "active"

    def get_categories(self):
        return list(set(models.Category.objects.all()))

    def get_category_types(self):
        categories = self.get_categories()
        types = []
        for c in categories:
            types.append(c.type_verbose())
        return list(set(types))

    def get_queryset(self):
        result = super(ListFoodsView, self).get_queryset()

        cat = self.request.GET.getlist('category')
        query = self.request.GET.get('q')
        exc = self.request.GET.get('exclude')

        if query:
            query_list = re.compile("^\s+|\s*,\s*|\s+$").split(query)
            self.search_text = ', '.join(query_list)
            result = result.filter(
                reduce(operator.or_,
                       (Q(ingredients__name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list))
            )
        if exc:
            query_list = re.compile("^\s+|\s*,\s*|\s+$").split(exc)
            self.exclude_text = ', '.join(query_list)
            result = result.exclude(
                reduce(operator.or_,
                       (Q(ingredients__name__icontains=q) for q in query_list)))
        if cat:
            result = result.filter(
                reduce(operator.or_,
                       (Q(category__name__icontains=q) for q in cat)))
            result = result.exclude(
                reduce(operator.or_,
                       (~Q(category__name__icontains=q) for q in cat)))
            self.checked_list = cat
        return result.distinct()


class ListCompareFoodsView(LoggedInMixin, ListView):
    model = models.DogFood
    paginate_by = 12
    page_title = _("Compare")
    template_name = 'doggyfood/compare.html'
    compared_dog_foods = []

    def get_ing_comparison(self):
        comp = set(self.compared_dog_foods[0].ingredients.all())
        for i in range(1, len(self.compared_dog_foods)):
            comp = comp & set(self.compared_dog_foods[i].ingredients.all()) & set(
                self.compared_dog_foods[i - 1].ingredients.all())
        #  set.intersection(*[set(..) for ... in ...])
        return list(comp)

    def get_queryset(self):
        result = super(ListCompareFoodsView, self).get_queryset()

        comp = self.request.GET.getlist('compare')

        if comp:
            result = result.filter(
                reduce(operator.or_,
                       (Q(pk=q) for q in comp)))
        self.compared_dog_foods = result.distinct()
        return result.distinct()


def preview_food(request, id):
    result = redirect_not_usr(request)
    if result:
        return result
    return render(request, "doggyfood/preview.html",
                  {
                      'object': models.DogFood.objects.filter(pk=id).first(),
                      'ingredients_composition': models.DogFood.objects.filter(
                          pk=id).first().get_ingredient_composition(),
                      'nutritional_composition': models.DogFood.objects.filter(
                          pk=id).first().get_nutritional_composition(),
                  }
                  )
