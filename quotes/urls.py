from django.urls import path
from django.conf import settings
from . import views


#URL Patterns
urlpatterns = [
  path(r'', views.home_page, name="home_page"),
  path(r'about', views.about, name="about_page"),
  path(r'show_all', views.show_all, name='show_all_page')
  
]
