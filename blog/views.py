from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random

# Create your views here.
class ShowAllView(ListView):
  '''Define a view class to show all blog articles'''

  model = Article
  template_name = "blog/show_all.html"
  context_object_name = "articles"

class ArticleView(DetailView):
  '''Display a single article'''

  model = Article
  template_name = "blog/article.html"
  context_object_name = 'article'

class RandomArticleView(DetailView):
  '''Display a random article '''
  model = Article
  template_name = "blog/article.html"
  context_object_name = 'article'

  # methods

  def get_object(self):
    '''return one instanec of the article object'''

    all_articles = Article.objects.all()
    article = random.choice(all_articles)
    return article