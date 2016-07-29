from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = "doggyfood"

urlpatterns = [
    url(r'^$', views.ListFoodsView.as_view(), name="list"),
    url(r'^about/$', TemplateView.as_view(template_name='doggyfood/about.html'), name="about"),
    url(r'^preview/(?P<pk>\d+)/$', views.DogfoodPreview.as_view(), name="preview"),
    url(r'^compare/$', views.ListCompareFoodsView.as_view(), name="compare"),
    url(r'^contact/$', views.contact, name='contact'),
]
