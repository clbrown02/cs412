from django.urls import path
from . import views

urlpatterns = [
  path(r'', views.VoterResultsView.as_view(), name='voter_home'),
  path(r'results', views.VoterResultsView.as_view(), name='voter_results_list'),
  path(r'voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),
  path(r'graphs', views.GraphView.as_view(), name = 'voter_graph')
]