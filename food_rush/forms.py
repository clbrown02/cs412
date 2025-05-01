# food_rush/forms.py  

from django import forms
from .models import Customer

class CreateCustomerForm(forms.ModelForm):
  '''A from to add a customer to the database'''

  class Meta:
    '''Associate this form with a model in our database'''
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
    