from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
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

  def get_object(self):
    '''Method to locate the user'''
    return get_object_or_404(Profile, user=self.request.user)

class CreateProfileView( CreateView):
  '''Define a create class to create a profile'''

  form_class = CreateProfileForm
  template_name ='mini_fb/create_profile_form.html'

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
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
  

class UpdateProfileView(LoginRequiredMixin, UpdateView):
  '''Defines a class that updates a profile'''

  model = Profile
  form_class = UpdateProfileForm
  template_name = 'mini_fb/update_profile_form.html'

  def get_object(self):
    """Retrieve the Profile of the currently logged-in user"""
    return get_object_or_404(Profile, user=self.request.user)

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
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

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
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

class AddFriendView(LoginRequiredMixin, View):
  '''View to add create a friend relationship between two profile objects'''
  def dispatch(self, request, *args, **kwargs):
    '''Read the URL parameters'''

    p1_pk = self.kwargs.get('pk')
    other_pk = self.kwargs.get('other_pk')

    p1 = get_object_or_404(Profile, pk=p1_pk)
    p2 = get_object_or_404(Profile, pk=other_pk)

    p1.add_friend(p2)

    return redirect('show_profile', pk=p1_pk)
  


class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    '''Shows friend suggestions for a profile'''
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"

    def get_object(self):
      """Retrieve the Profile of the currently logged-in user"""
      return get_object_or_404(Profile, user=self.request.user)

class ShowNewsFeedView(DetailView):
    '''View to show a personalized news feed'''
    model = Profile
    template_name = "mini_fb/news_feed.html"

    def get_object(self):
        """Retrieve the Profile of the currently logged-in user"""
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["news_feed"] = profile.get_news_feed()
        return context