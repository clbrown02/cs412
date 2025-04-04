from django.urls import path
from . import views

urlpatterns = [
  path(r'', views.VoterResultsView.as_view(), name='voter_home'),
  path(r'results', views.VoterResultsView.as_view(), name='voter_results_list'),
  path('voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),
]