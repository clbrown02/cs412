from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import ListView
from . models import Result
# Create your views here.

class ResultsListView(ListView):
  '''View to display marathon results'''

  model = Result
  template_name = 'marathon_analytics/results.html'
  context_object_name = 'results'
  paginate_by = 25

  def get_queryset(self):
    '''limit the queryset for now'''
    results = super().get_queryset()
    #return results[:25]

    if 'city' in self.request.GET:
      city = self.request.GET['city']

      if city:
        results = results.filter(city=city)
    
    return results