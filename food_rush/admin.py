from django.contrib import admin

# Register your models here.

from .models import Customer, Restaurant, Food_item, Food_selection, Order
admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(Food_item)
admin.site.register(Food_selection)
admin.site.register(Order)
