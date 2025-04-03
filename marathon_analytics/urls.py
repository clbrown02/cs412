from django.urls import path
from . import views

urlpatterns = [
  path(r'', views.ResultsListView.as_view(), name='mar_home'),
  path(r'results', views.ResultsListView.as_view(), name='mar_results_list'),
]