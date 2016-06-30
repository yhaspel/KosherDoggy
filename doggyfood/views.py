from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.encoding import escape_uri_path
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _

from . import models

# Create your views here.




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

    # def get_queryset(self):
    #     return super().get_queryset().filter(account__user=self.request.user)
    #
    # def total(self):
    #     return self.get_queryset().aggregate(sum=Sum('amount'))['sum']