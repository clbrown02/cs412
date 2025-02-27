from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
  '''Encapsulate the data of a mini_fb profile'''

  first_name = models.TextField(blank=True)
  last_name = models.TextField(blank=True)
  city = models.TextField(blank=True)
  email = models.EmailField(blank=True)
  profile_image_url = models.URLField(blank=True)

  def __str__(self):
    '''Return a String representation of the Profile object'''
    return f'{self.first_name} {self.last_name}'
  
  def get_status_messages(self):
    '''Return status messages associated with associated profile'''
    status_message = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    return status_message
  
  def get_absolute_url(self):
    '''Provide a URL after creating a new Profile'''
    return reverse('show_profile', kwargs={'pk':self.pk})

  
class StatusMessage(models.Model):
  '''Encapsulates the data of a status message'''

  timestamp = models.DateTimeField(auto_now=True)
  message = models.TextField(blank=True)
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

  def __str__(self):
    '''Returns a string representation of the status message object'''
    return f'{self.message}'