from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
  '''Encapsulate the data of a mini_fb profile'''

  first_name = models.TextField(blank=True)
  last_name = models.TextField(blank=True)
  city = models.TextField(blank=True)
  email = models.EmailField(blank=True)
  profile_image_url = models.URLField(blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    '''Return a String representation of the Profile object'''
    return f'{self.first_name} {self.last_name}'
  
  def get_status_messages(self):
    '''Return status messages associated with associated profile'''
    status_message = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    return status_message
  
  def get_friends(self):
    '''Return a list of friend's profiles '''
    friends = []
    for friend in Friend.objects.filter(profile1=self):
      friends.append(friend.profile2)
    
    for friend in Friend.objects.filter(profile2=self):
      friends.append(friend.profile1)
    
    return friends
  
  def add_friend(self, other):
    '''Method that creates a friend relationship between self and other profile object'''
    if self == other:
      return "Error: You cant friend yourself"
    
    already_friends = Friend.objects.filter(profile1=self, profile2=other).exists() or Friend.objects.filter(profile1=other, profile2=self).exists()

    if already_friends:
      return "You are already friends with this person"
    
    Friend.objects.create(profile1=self, profile2=other)
    return f"{other} is now your friend"
  
  def get_friend_suggestions(self):
    """Returns a list of possible friends for a profile"""
  
    friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2__pk', flat=True)   
    friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1__pk', flat=True)
    
    friend_ids = set(friends_as_profile1) | set(friends_as_profile2)

    suggestions = Profile.objects.exclude(pk__in=friend_ids).exclude(pk=self.pk)

    return suggestions
  
  def get_news_feed(self):
        '''Returns a QuerySet of status messages from self and friends, ordered by most recent'''
        friend_profiles = self.get_friends()  
    
        news_feed = StatusMessage.objects.filter(profile__in=friend_profiles).order_by('-timestamp')
        
        return news_feed

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
  
  def get_images(self):
    '''Returns a Queryset of Images related to a Status Message '''
    status_image = StatusImage.objects.filter(status_message=self)
    return status_image
  
class Image(models.Model):
  '''Encapsulates the data of an Image'''

  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  image_file = models.ImageField(blank=True)
  timestamp = models.DateTimeField(auto_now=True)


class StatusImage(models.Model):
  '''Models the relationship betweem Images and StatusMessage'''

  image = models.ForeignKey(Image, on_delete=models.CASCADE)
  status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)

class Friend(models.Model):
  '''Encapsulates the idea of an edge connecting two nodes within the social network'''
  profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
  profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
  timestamp = models.DateTimeField(auto_now=True)

  def __str__(self):
    '''Method to view this relationship as a string representation'''
    return f'{self.profile1} & {self.profile2}'