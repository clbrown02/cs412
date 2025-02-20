from django.urls import path
from .views import ShowAllView, ArticleView, RandomArticleView

urlpatterns = [
  path('', RandomArticleView.as_view(), name="random"),
  path('article/<int:pk>', ArticleView.as_view(), name="article"),
  path('show_all', ShowAllView.as_view(), name="show_all"),
]