from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

class ShowAllProfilesView(ListView):
  '''Define a show class to show all profiles'''

  model = Profile
  template_name = "mini_fb/show_all_profiles.html"
  context_object_name = "profiles"