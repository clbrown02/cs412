
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse
# Create your views here.

class ShowAllRestaurantsView(ListView):
  '''Define a show class to show all restaurants'''

  model = Restaurant
  template_name = 'food_rush/show_all_restaurants.html'
  context_object_name = 'restaurants'

class ShowRestaurantView(DetailView):
  '''Define a show class to show a single restaurant'''

  model = Restaurant
  template_name = 'food_rush/show_restaurant.html'
  
  def get_context_data(self, **kwargs):
    ctx = super().get_context_data(**kwargs)
    ctx["foods"] = self.object.food_item_set.all()
    
    return ctx
