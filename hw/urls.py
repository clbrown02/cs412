from django.urls import path
from django.conf import settings
from . import views


#URL Patterns
urlpatterns = {
  path(r'', views.home, name="home"),
}
