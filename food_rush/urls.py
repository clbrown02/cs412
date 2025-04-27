# food_rush/urls.py 

from django.urls import path
from .views import *

urlpatterns = [
  path('', ShowAllRestaurantsView.as_view(), name='show_restaurants'),
  path('restaurant/<int:pk>/', ShowRestaurantView.as_view(), name='show_restaurant'),
  path("cart/add/", add_to_cart, name="cart_add"),
  path("cart/", CartView.as_view(), name="cart_view"),
  path("checkout/", CheckoutView.as_view(), name="checkout"),
  path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail" ),
]

