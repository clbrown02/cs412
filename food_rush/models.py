# food_rush/models.py

from django.db import models
import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

class Customer(models.Model):
  '''Encapsulates the idea of a Customer model'''

  # data attributes of a customer
  first_name = models.TextField(blank=False)
  last_name = models.TextField(blank=False)
  email = models.EmailField(blank=True)
  phone_number = models.CharField(max_length=12)
  user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer",   # singular
    )

  def __str__(self):
    '''Return a string represenation of this Customer object'''
    return f'{self.first_name}  {self.last_name}'
  
  def get_order_history(self):
     '''Return a Queryset of past orders associated with this Customer object'''
     orders = []
     for order in Order.objects.filter(customer=self):
        orders.append(order)
    
     return orders
  
  def get_absolute_url(self):
     '''Provide a URL after creating a new customer'''
     return reverse('show_restaurants')

class Restaurant(models.Model):
  '''Encapsulates the idea of a Restaurant model'''

  # data attributes of a restaurant
  name = models.TextField(blank=False)
  address = models.TextField(blank=False)
  profile_photo = models.ImageField(blank=True)
  opening_time = models.TimeField(blank=False)
  closing_time = models.TimeField(blank=False)

  def __str__(self):
    '''Return a string representation of this Restaurant object'''
    return f'{self.name}'
  
class Food_item(models.Model):
  '''Encapsulates the idea of a food item model'''

  #data attributes of a food item
  name = models.TextField(blank=False)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=5,decimal_places=2)
  description = models.TextField(blank=False)
  food_photo = models.ImageField(blank=True)

  def __str__(self):
    '''Return a string representation of this Food_item object'''
    return f'{self.name}'
  
class Food_selection(models.Model):
  '''Encapsulates the idea of a food selection model'''

  #data attributes of a food item
  order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="selections")
  item = models.ForeignKey(Food_item, on_delete=models.PROTECT)
  quantity = models.PositiveIntegerField(default=1)
  price_at_order = models.DecimalField(max_digits=7, decimal_places=2)

  def line_total(self):
     return self.quantity * self.price_at_order

  def __str__(self):
    '''Returns a string representation of this Food_selection object'''
    return f'{self.item.name} x {self.quantity} (Order #{self.order.id})'

  # Checks if the item is from the same restaurant as the one the order was placed
  def clean(self):
        super().clean()
        if self.order and self.item:
            if self.order.restaurant_id != self.item.restaurant_id:
                raise ValidationError(
                    "That menu item belongs to a different restaurant "
                    "than the one this order was placed at."
                )

  # Call the save function whenever saving a food selection object
  def save(self, *args, **kwargs):
      self.full_clean()     
      return super().save(*args, **kwargs)
  



class Order(models.Model):
  '''Encapsulates the idea of a order model'''

  #data attributes of a order item
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
  order_date = models.DateTimeField(editable=False)
  eta = models.DateTimeField(editable=False)
  food = models.ManyToManyField(Food_item, through=Food_selection, related_name='orders')

  def save(self, *args, **kwargs):
     if not self.pk:
        now = timezone.now()
        self.order_date = now
        self.eta = now + timedelta(minutes=random.randint(15,30))
     super().save(*args,**kwargs)

  def __str__(self):
    '''Returns a string representation of this order object'''
    return f'Order #{self.id} - {self.customer}'
  
  @property
  def total(self):
     '''Returns the toal cost of the order'''
     return sum(sel.line_total() for sel in self.selections.all())
  



  
  
  


