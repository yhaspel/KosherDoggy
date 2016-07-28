from django.conf.urls import url

from . import views

app_name = "doggyfood"

urlpatterns = [
    url(r'^$', views.ListFoodsView.as_view(), name="list"),
    # url(r'^preview/(?P<id>\d+)/$', views.preview_food, name="preview"),
    url(r'^preview/(?P<pk>\d+)/$', views.DogfoodPreview.as_view(), name="preview"),
    url(r'^compare/$', views.ListCompareFoodsView.as_view(), name="compare"),
    # url(r'^add-account/$', views.CreateAccountView.as_view(),
    #     name="create_account"),
    # url(r'^add-expense/$', views.CreateExpenseView.as_view(), name="create"),
]
