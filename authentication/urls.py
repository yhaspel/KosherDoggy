from django.conf.urls import url
from . import views

app_name = "authentication"
urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.register_user, name="register"),
    url(r'^password_change/$', views.password_change, name="password_change"),
]
