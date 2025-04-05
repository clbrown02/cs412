from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from . models import Voter
import datetime
import pandas as pd
import plotly.express as px
from django.db.models import Count
from django.db.models.functions import ExtractYear



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

class GraphView(ListView):
   '''Class to display voter analytics in a graph/chart'''

   model = Voter
   template_name = 'voter_analytics/graphs.html'
   context_object_name = 'voters'
   paginate_by = 100

   def get_context_data(self, **kwargs):
      '''Method to obtain context_data'''

      context = super().get_context_data(**kwargs)

      birth_qs = Voter.objects.annotate(year=ExtractYear('dob')).values('year').annotate(count=Count('id')).order_by('year')
      df_birth = pd.DataFrame(list(birth_qs))
      if not df_birth.empty:
          fig_birth = px.bar(
              df_birth,
              x='year',
              y='count',
              title='Distribution of Voters by Year of Birth',
              labels={'year': 'Year of Birth', 'count': 'Number of Voters'}
          )
          birth_chart_html = fig_birth.to_html(full_html=False)
      else:
          birth_chart_html = "<p>No data available</p>"
      context['birth_chart_html'] = birth_chart_html


      party_qs = Voter.objects.values('party').annotate(count=Count('id'))
      df_party = pd.DataFrame(list(party_qs))
      if not df_party.empty:
          fig_party = px.pie(
              df_party,
              names='party',
              values='count',
              title='Voter Party Affiliation'
          )
          party_chart_html = fig_party.to_html(full_html=False)
      else:
          party_chart_html = "<p>No data available</p>"
      context['party_chart_html'] = party_chart_html

      
      election_counts = {
          'v20': Voter.objects.filter(v20__iexact="TRUE").count(),
          'v21_t': Voter.objects.filter(v21_t__iexact="TRUE").count(),
          'v21_p': Voter.objects.filter(v21_p__iexact="TRUE").count(),
          'v22': Voter.objects.filter(v22__iexact="TRUE").count(),
          'v23': Voter.objects.filter(v23__iexact="TRUE").count(),
      }
      df_election = pd.DataFrame(list(election_counts.items()), columns=['Election', 'Count'])
      if not df_election.empty:
          fig_election = px.bar(
              df_election,
              x='Election',
              y='Count',
              title='Voter Participation by Election',
              labels={'Election': 'Election', 'Count': 'Number of Voters'}
          )
          election_chart_html = fig_election.to_html(full_html=False)
      else:
          election_chart_html = "<p>No data available</p>"
      context['election_chart_html'] = election_chart_html

      current_year = datetime.date.today().year
      context['years'] = list(range(1900, current_year + 1))
      context['score_range'] = list(range(0, 5))

      return context