# food_rush/urls.py 

from django.urls import path
from .views import *

urlpatterns = [
  path('', ShowAllRestaurantsView.as_view(), name='show_restaurants'),
  path('restaurant/<int:pk>', ShowRestaurantView.as_view(), name='show_restaurant'),
]