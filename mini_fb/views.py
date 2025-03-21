from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
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

    sm = form.save()
    files = self.request.FILES.getlist('files')

    for file in files:
      image = Image(profile=profile, image_file =file)
      image.save()

      status_image = StatusImage(image=image, status_message=sm)
      status_image.save()


    return super().form_valid(form)
  
  def get_success_url(self):
    '''Provide a URL to redirect to after creating a new status message'''
    pk = self.kwargs['pk']

    return reverse('show_profile', kwargs={'pk': pk})
  

class UpdateProfileView(UpdateView):
  '''Defines a class that updates a profile'''

  model = Profile
  form_class = UpdateProfileForm
  template_name = 'mini_fb/update_profile_form.html'

class DeleteStatusMessageView(DeleteView):
  '''Class to delete a status message'''
  model = StatusMessage
  template_name = "mini_fb/delete_status_form.html"
  context_object_name = 'statusmessage'

  def get_success_url(self):
    '''Return the URL to redirect to after a succesful delete'''
    pk = self.kwargs['pk']

    status_message = StatusMessage.objects.get(pk=pk)

    profile = status_message.profile

    return reverse('show_profile', kwargs={'pk':profile.pk})

class UpdateStatusMessageView(UpdateView):
  '''Defines a class that updates a statusmessage'''

  model = StatusMessage
  form_class = UpdateStatusMessageForm
  template_name = "mini_fb/update_status_message_form.html"

  def get_success_url(self):
    '''Return the URL to redirect to after a successful update'''
    pk = self.kwargs['pk']

    status_message = StatusMessage.objects.get(pk=pk)

    profile = status_message.profile

    return reverse('show_profile', kwargs={'pk':profile.pk})
