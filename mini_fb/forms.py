from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
  '''A form to add a Profile to the database'''

  class Meta:
    '''Associate this form with a model in our database'''
    model = Profile
    fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url' ]


class CreateStatusMessageForm(forms.ModelForm):
  '''A form to add a Status Message to a Profile'''

  class Meta:
    '''Associate this form with a model in our database'''
    model = StatusMessage
    fields = ['message']

class UpdateProfileForm(forms.ModelForm):
  '''A form that updates a Profile'''

  class Meta:
    '''Associate this form with a model in our db'''
    model = Profile
    fields = ['city', 'email', 'profile_image_url']

class UpdateStatusMessageForm(forms.ModelForm):
  '''A form that updates a StatusMessage'''
  
  class Meta:
    '''Associate this form with a model in our DB'''
    model = StatusMessage
    fields = ['message']