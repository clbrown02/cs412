from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
quotes = []


def home_page(request):
   template_name = 'quotes/quote.html'
   context = {}
# make sure to add context to render
   return render(request, template_name)


def about(request):
   tempplate_name = 'quotes/about.html'
   context = {}

   return render(request, tempplate_name)