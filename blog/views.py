from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse
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


# define a subclass of CreateView to handle creation of Article objects
class CreateArticleView(CreateView):
  '''A view to handle creation of a new article.
  (1) display the HTML form to user (GET)
  (2) process the form submission and store the new Article object (POST)
    '''
  
  form_class = CreateArticleForm
  template_name = "blog/create_article_form.html"

class CreateCommentView(CreateView):
  '''A view to handle creation of a new Comment on an article'''

  form_class = CreateCommentForm
  template_name = "blog/create_comment_form.html"

  def get_success_url(self):
    '''Provide a URL to redirect to after creating a new comment '''
    pk = self.kwargs['pk']
    return reverse('article', kwargs={'pk':pk})
   
  def get_context_data(self):
    '''Return the dictionary of context variables for use in the template'''

    context = super().get_context_data()

    # retrieve the PK from the URL pattern
    pk = self.kwargs['pk']
    article = Article.objects.get(pk=pk)

    context['article'] = article

    return context


  def form_valid(self, form):
    '''This method handles the form submission and saves the new object to the Django DB
    We need to add the foreign key (of the Article) to the Comment object before saving it to the database.
    '''
    
    print(form.cleaned_data)
    # retrieve the PK from the URL pattern
    pk = self.kwargs['pk']
    article = Article.objects.get(pk=pk)
    # attach this article to the comment
    form.instance.article = article 

    # delegate the work to the superclass mehod form_valid

    return super().form_valid(form)