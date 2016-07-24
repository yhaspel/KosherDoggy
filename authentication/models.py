from django.db import models
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.encoding import escape_uri_path


class LoggedInMixin:
    def dispatch(self, request, *args, **kwargs):
        result = redirect_not_usr(request)
        return result if result else super().dispatch(request, *args, **kwargs)


def redirect_not_usr(request):
    if not request.user.is_authenticated():
        url = reverse("authentication:login") + "?from=" + escape_uri_path(request.path)
        return redirect(url)
    else:
        return False

