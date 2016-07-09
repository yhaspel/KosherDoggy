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
from django.views.generic.detail import DetailView
# from authentication.models import LoggedInMixin, redirect_not_usr

from . import models


class LoggedInMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            url = reverse("login") + "?from=" + escape_uri_path(request.path)
            return redirect(url)
        return super().dispatch(request, *args, **kwargs)


class ListFoodsView(ListView):
    model = models.DogFood
    paginate_by = 12
    page_title = _("Home")

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
        # cat = self.request.POST.getlist('category')
        query = self.request.GET.get('q')
        exc = self.request.GET.get('exclude')

        if query:
            # query_list = query.split()
            query_list = re.compile("^\s+|\s*,\s*|\s+$").split(query)
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
            result = result.exclude(
                reduce(operator.or_,
                       (Q(ingredients__name__icontains=q) for q in query_list)))

        if cat:
            query_list = re.compile("^\s+|\s*,\s*|\s+$").split(cat)
            # query_list = cat.split();
            messages.success(self.request, query_list)
            result = result.filter(
                reduce(operator.or_,
                       (Q(category__name__icontains=q) for q in query_list)))
            result = result.exclude(
                reduce(operator.or_,
                       (~Q(category__name__icontains=q) for q in query_list)))

        return result.distinct()


def preview_food(request, id):
    # result = redirect_not_usr(request)
    # if result:
    #     return result
    return render(request, "doggyfood/preview.html",
                  {
                      'object': models.DogFood.objects.filter(pk=id).first()
                  }
                  )
