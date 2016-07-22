import operator
from functools import reduce

import re
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.encoding import escape_uri_path
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
# from authentication.models import LoggedInMixin, redirect_not_usr
from django.views.generic.edit import FormMixin

from doggyfood.models import DogFood
from . import models


class LoggedInMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            url = reverse("login") + "?from=" + escape_uri_path(request.path)
            return redirect(url)
        return super().dispatch(request, *args, **kwargs)


class FormListView(ListView, FormMixin):
    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    # TODO: here's the problem. Post get there, how to update 'compare' BooleanField?
    def post(self, request, *args, **kwargs):

        dogfood = DogFood.objects.all().first()
        if dogfood.compare == True:
            dogfood.compare = False
        else:
            dogfood.compare = True
        dogfood.save()
        test1 = self.get(request, *args, **kwargs)
        messages.success(request, test1)  # TODO: remove
        # if self.request.POST.get('compare', False):
        #     messages.success(request, "TEST 2")
        #     self.request.POST['compare'] = True
        return self.get(request, *args, **kwargs)


class ListFoodsView(ListView):
    model = models.DogFood
    paginate_by = 12
    page_title = _("Home")
    search_text = ''
    exclude_text = ''


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

        cat = self.request.GET.get('category')
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
            query_list = re.compile("^\s+|\s*,\s*|\s+$").split(cat)
            result = result.filter(
                reduce(operator.or_,
                       (Q(category__name__icontains=q) for q in query_list)))
            result = result.exclude(
                reduce(operator.or_,
                       (~Q(category__name__icontains=q) for q in query_list)))
            self.search_text += '; Categories: ' + ', '.join(query_list)

        return result.distinct()


# TODO: complete this after checkbox post is functional
class ListCompareFoodsView(ListView):
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
    # result = redirect_not_usr(request)
    # if result:
    #     return result
    return render(request, "doggyfood/preview.html",
                  {
                      'object': models.DogFood.objects.filter(pk=id).first(),
                      'ingredients_composition': models.DogFood.objects.filter(
                          pk=id).first().get_ingredient_composition(),
                      'nutritional_composition': models.DogFood.objects.filter(
                          pk=id).first().get_nutritional_composition(),
                  }
                  )
