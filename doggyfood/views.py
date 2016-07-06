import operator
from functools import reduce

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

    def get_queryset(self):
        result = super(ListFoodsView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(ingredients__name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list))
            )

        return result.distinct()

    # def get_queryset(self):
    #     return super().get_queryset().filter(id=1)

    # def sommodel_list(self):
    #     return SomeModel.objects.all()

    # def get_queryset(self):
    #     res = super().get_queryset().filter(ingredient=models.Ingredient.get(id=self.kwargs['ingredient'])
    #     return res
    #
    # def total(self):
    #     return self.get_queryset().aggregate(sum=Sum('amount'))['sum']


def preview_food(request, id):
    # result = redirect_not_usr(request)
    # if result:
    #     return result
    return render(request, "doggyfood/preview.html",
                  {
                      'object': models.DogFood.objects.filter(pk=id).first()
                  }
                  )
