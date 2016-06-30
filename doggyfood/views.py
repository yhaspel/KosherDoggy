from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.encoding import escape_uri_path
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _

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

    # def sommodel_list(self):
    #     return SomeModel.objects.all()
    #
    # def get_queryset(self):
    #     res = super().get_queryset().filter(ingredient=models.Ingredient.get(id=self.kwargs['ingredient'])
    #     return res
        #
        # def total(self):
        #     return self.get_queryset().aggregate(sum=Sum('amount'))['sum']

