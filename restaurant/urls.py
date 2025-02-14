from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
  path(r'', views.home_page, name="home_page"),
  path(r'main', views.home_page, name="main_page"),
  path(r'order', views.order_page, name='order_page'),
]