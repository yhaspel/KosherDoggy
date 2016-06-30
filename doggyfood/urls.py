from django.conf.urls import url

from . import views

app_name = "doggyfood"

urlpatterns = [
    url(r'^$', views.ListFoodsView.as_view(), name="list"),
    # url(r'^dummy/$', views.DummyView.as_view(), name="dummy"),
    # url(r'^(?P<pk>\d+)/$', views.ExpenseDetailView.as_view(), name="detail"),
    # url(r'^add-account/$', views.CreateAccountView.as_view(),
    #     name="create_account"),
    # url(r'^add-expense/$', views.CreateExpenseView.as_view(), name="create"),
]
