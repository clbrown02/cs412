from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def show_form(request):
  '''Show form to the user'''

  template_name = 'formdata/form.html'
  return render(request, template_name)

def submit(request):

  template_name = "formdata/confirmation.html"
  print(request.POST)

  if request.POST:
    # Extracts fields into variables
    name = request.POST['name']
    favorite_color = request.POST['color']

    context = {
      'name': name,
      'favorite_color': favorite_color,
    }

  return render(request, template_name=template_name, context=context)