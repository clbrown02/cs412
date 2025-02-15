from django.shortcuts import render
from django.http import HttpResponse
import random
from datetime import datetime, timedelta

dailys = [
  "Horchata", "Agua de Jamaica", "Torta",
  "Cheesy Gordita Dorito Crunch Wrap Supreme"
]

prices = {
  'Six beef tacos': 9,
  'Six tripa tacos': 9,
  'Charro beans': 6,
  'Quesabirria': 8,
  'Guacamole': 4,
  'Grilled onions': 2,
  'Salsas': 0,
  'Corn tortillas': 1,
  'Horchata': 5,
  'Agua de Jamaica': 4,
  'Torta': 6,
  'Cheesy Gordita Dorito Crunch Wrap Supreme': 10
}



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

def confirmation(request):
  template_name = 'restaurant/confirmation.html'


  print(request.POST)

  if request.POST:
    item1 = request.POST.getlist('item1')
    extra = request.POST.getlist('extra')
    special = request.POST.getlist('special')
    requests = request.POST.getlist('requests')
    name = request.POST.getlist('name')
    phone = request.POST.getlist('phone')
    email = request.POST.getlist('email')

  cost = 0
  order =""

  for item in item1:
    print(item)
    cost += prices[item]
    order += item + ", "


  for item in extra:
    print(item)
    cost += prices[item]
    order += item + ", "

  for item in special:
    order += item 
    cost += prices[item]



  min_mins = 30
  max_mins = 60
  rand_mins = random.randint(min_mins, max_mins)

  exp_time = datetime.now() + timedelta(minutes=rand_mins)
  exp_time = exp_time.strftime("%a %b %d %H:%M:%S %Y")

  context = {
    'order': order,
    'cost': cost,
    'requests': requests[0],
    'name': name[0],
    'phone': phone[0],
    'email': email[0],
    'exp_time': exp_time
  }


  return render(request, template_name, context)