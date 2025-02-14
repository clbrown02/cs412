from django.shortcuts import render
from django.http import HttpResponse
import random

dailys = [
  "Horchata  ($5)", "Agua de Jamaica  ($4)", "Torta  ($6)",
  "Cheesy Gordita Dorito Crunch Wrap Supreme  ($10)"
]



def home_page(request):
  template_name = 'restaurant/main.html'

  return render(request, template_name)

def order_page(request):

  random_index = random.randint(0, len(dailys)-1)
  random_daily = dailys[random_index]

  context = {
    "random_daily": random_daily
  }

  template_name = 'restaurant/order.html'

  return render(request, template_name, context)