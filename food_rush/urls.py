# food_rush/urls.py 

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('', ShowAllRestaurantsView.as_view(), name='show_restaurants'),
  path('restaurant/<int:pk>/', ShowRestaurantView.as_view(), name='show_restaurant'),
  path("cart/add/", add_to_cart, name="cart_add"),
  path("cart/", CartView.as_view(), name="cart_view"),
  path("cart/clear/", clear_cart, name="cart_clear"),
  path("checkout/", CheckoutView.as_view(), name="checkout"),
  path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail" ),
  path('create_customer/', CreateProfileView.as_view(), name='create_customer'),
  path('login', auth_views.LoginView.as_view(template_name='food_rush/login.html'), name='food_rush_login' ),
  path('logout/', auth_views.LogoutView.as_view(template_name='food_rush/food_rush_logged_out.html', next_page='food_rush_logged_out.html'), name='food_rush_logout'),
  path('order_history/', ShowOrderHistoryView.as_view(), name="order_history"),
]

