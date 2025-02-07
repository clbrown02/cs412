from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Create your views here.
quotes = ["I could let these dream killers kill my self-esteem or use my arrogance as the steam to power my dreams",
          "Im not out of control, I'm just not in they control.",
          "I'm nice at ping pong.",
          "I hate when I’m on a flight and I wake up with a water bottle next to me like oh great now I gotta be responsible for this water bottle."]
images = ['kanye_closeup.jpg', 'kanye_donda.jpeg', 'kanye_graduation.jpg', 'kanye_professional.jpg' ]



def home_page(request):

   random_index = random.randint(0, len(quotes) -1)
   random_quote = quotes[random_index]
   random_image = images[random_index]


   template_name = 'quotes/quote.html'
   context = {
      'selected_quote': random_quote,
      'selected_image': random_image ,
      }
# make sure to add context to render
   return render(request, template_name, context)


def about(request):
   tempplate_name = 'quotes/about.html'
   context = {}

   return render(request, tempplate_name)