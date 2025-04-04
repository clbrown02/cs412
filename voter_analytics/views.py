from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from . models import Voter
import datetime

# Create your views here.
class VoterResultsView(ListView):
  '''View to display all voters records in a list format'''

  model = Voter
  template_name = 'voter_analytics/results.html'
  context_object_name = 'results'
  paginate_by = 100

  def get_queryset(self):
    '''limit the queryset for now'''
    results = super().get_queryset()
    #return results[:25]

    if 'party' in self.request.GET:
      affiliation = self.request.GET['party']

      if affiliation:
        results = results.filter(party=affiliation)
    
    if 'score' in self.request.GET:
      score = self.request.GET['score']

      if score:
        results = results.filter(voter_score=score)

    if 'min_dob' in self.request.GET:
      min_dob = self.request.GET['min_dob']

      if min_dob:
        results = results.filter(dob__year__gte=min_dob)

    if 'max_dob' in self.request.GET:
      max_dob = self.request.GET['max_dob']

      if max_dob:
        results = results.filter(dob__year__lte=max_dob)

    for election in ['v20', 'v21_t', 'v21_p', 'v22', 'v23']:
            if self.request.GET.get(election) == 'True':
                results = results.filter(**{election: 'TRUE'})  # or use True if BooleanField

    
    
    return results
  
  def get_context_data(self, **kwargs):
    '''Providing the context data '''
    context = super().get_context_data(**kwargs)

    curr_year = datetime.date.today().year
    context['years'] = list(range(1900, curr_year + 1))

    return context
  
class VoterDetailView(DetailView):
    '''Class to showcase a single voters profile'''
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'