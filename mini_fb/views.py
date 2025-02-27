from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse

class ShowAllProfilesView(ListView):
  '''Define a show class to show all profiles'''

  model = Profile
  template_name = "mini_fb/show_all_profiles.html"
  context_object_name = "profiles"

class ShowProfilePageView(DetailView):
  '''Define a show class to show one profile'''

  model = Profile
  template_name = "mini_fb/show_profile.html"
  context_object_name = "profile"

class CreateProfileView(CreateView):
  '''Define a create class to create a profile'''

  form_class = CreateProfileForm
  template_name ='mini_fb/create_profile_form.html'

class CreateStatusMessageView(CreateView):
  '''Define a create class to create a profile'''

  form_class = CreateStatusMessageForm
  template_name = 'mini_fb/create_status_form.html'

  def get_context_data(self):
    '''Function to get the PK of the status message profile'''
    context = super().get_context_data()

    pk = self.kwargs['pk']
    profile = Profile.objects.get(pk=pk)


    context['profile'] = profile

    return context

  def form_valid(self, form):
    '''Function to check whether the form is valid'''
    profile = Profile.objects.get(pk=self.kwargs['pk'])

    form.instance.profile = profile
    return super().form_valid(form)
  
  def get_success_url(self):
    '''Provide a URL to redirect to after creating a new status message'''
    pk = self.kwargs['pk']

    return reverse('show_profile', kwargs={'pk': pk})
  

