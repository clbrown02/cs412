from django.db import models

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