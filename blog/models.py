from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
class Article(models.Model):
  '''Encapsulate the data of a blog article by an author'''

  # data attributes
  title = models.TextField(blank=True)
  author = models.TextField(blank=True)
  text = models.TextField(blank=True)
  published = models.DateTimeField(auto_now=True)
  # image_url = models.URLField(blank=True)
  image_file = models.ImageField(blank=True)
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  
  def __str__(self):
    '''return a string representation of this model'''
    return f'{self.title} by  {self.author}'
  
  def get_absolute_url(self):
    '''Return the URL to display one instance of this object'''
    return reverse('article', kwargs={'pk': self.pk})
  
  def get_all_comments(self):
    '''Return a Queryset of comments about this article'''
    comments = Comment.objects.filter(article=self)
    return comments

  
class Comment(models.Model):
  '''Encapsulate the idea of a Comment'''

  # data attributes for the comment:
  article = models.ForeignKey(Article, on_delete=models.CASCADE)
  author = models.TextField(blank=False)
  text = models.TextField(blank=False)
  published = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    '''Return a string representation of this Comment'''
    return f'{self.text}'