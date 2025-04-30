
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .forms import *
# Create your views here.



class ShowAllRestaurantsView(ListView):
  '''Define a show class to show all restaurants'''

  model = Restaurant
  template_name = 'food_rush/show_all_restaurants.html'
  context_object_name = 'restaurants'

class ShowRestaurantView(DetailView):
  '''Define a show class to show a single restaurant'''

  model = Restaurant
  template_name = 'food_rush/show_restaurant.html'
  
  def get_context_data(self, **kwargs):
    ctx = super().get_context_data(**kwargs)
    ctx["foods"] = self.object.food_item_set.all()
    
    return ctx

def add_to_cart(request):
  '''method to add items to session cart'''
  food_id = int(request.POST["food_id"])
  qty = int(request.POST.get("qty", 1))
  food = get_object_or_404(Food_item, pk=food_id)

  cart = request.session.get("cart", {})
  rest_id_in_cart = cart.get("restaurant_id")

  if rest_id_in_cart in (None, food.restaurant_id):
        cart.setdefault("items", {})
        cart["restaurant_id"] = food.restaurant_id
        cart["items"][str(food_id)] = cart["items"].get(str(food_id), 0) + qty
        request.session["cart"] = cart
        messages.success(request, "Added to cart.")
  else:
      messages.error(
          request,
          "You already have items from another restaurant. "
          "Finish or empty that order first."
      )
  # back to the page we came from
  return redirect(request.META.get("HTTP_REFERER",
                    reverse("show_restaurant", args=[food.restaurant_id])))

class CartView(TemplateView):
   '''Define a show class that displays a form'''
   template_name = "food_rush/cart.html"

   def get_context_data(self, **kwargs):
      ctx = super().get_context_data(**kwargs)
      cart = self.request.session.get("cart", {})
      rest_id = cart.get("restaurant_id")
      ctx["current_restaurant"] = Restaurant.objects.filter(pk=rest_id).first()
      items, total = [], 0
      for fid, qty in cart.get("items", {}).items():
         food = get_object_or_404(Food_item, pk=int(fid))
         line = {
            "food": food,
            "qty": qty,
            "subtotal": food.price * qty
         }
         total += line["subtotal"]
         items.append(line)
        #  sub = food.price * qty
        #  total += sub
        #  items.append({"food": food, "qty": qty, "subtotal": sub})
      ctx.update({"items": items, "total": total})
      return ctx
# @require_POST
# def checkout(request):
#    '''Create the order item'''
#    cart = request.session.get("cart")
#    if not cart or not cart.get("items"):
#       messages.error(request, "Your cart is empty.")
#       return redirect("show_all_restaurants")
   
#    restaurant = get_object_or_404(Restaurant, pk=cart["restaurant_id"])
#    order = Order.objects.create(customer=request.user.customer, restaurant=restaurant)

#    food_selections = []
#    for fid, qty in cart["items"].items():
#       food = get_object_or_404(Food_item, pk=int(fid))
#       food_selections.append(
#          Food_selection(
#           order = order,
#           item = get_object_or_404(Food_item, pk=int(fid)),
#           quantity = qty,
#           price_order = food.price)
#       )

#       Food_selection.objects.bulk_create(food_selections)

#       request.session.pop("cart", None)
#       messages.success(request, f"Order #{order.pk} placed! ETA: {order.eta.astimezone().strftime('%H:%M')}.")
#       return redirect("order_detail", pk=order.pk)

class CheckoutView(View):
    http_method_names = ["post"]

    @method_decorator(login_required)
    @method_decorator(require_POST)
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        cart = request.session.get("cart") or {}
        if not cart.get("items"):
            messages.error(request, "Cart is empty.")
            return redirect("cart_view")

        # ensure user→customer link exists
        try:
            
            customer = request.user.customer
        except Customer.DoesNotExist:
            messages.error(request, "No customer profile.")
            return redirect("cart_view")

        restaurant = get_object_or_404(Restaurant, pk=cart["restaurant_id"])
        order = Order.objects.create(customer=customer, restaurant=restaurant)

        selections = []
        for fid, qty in cart["items"].items():
            food = get_object_or_404(Food_item, pk=int(fid))
            selections.append(
                Food_selection(
                    order=order,
                    item=food,
                    quantity=qty,
                    price_at_order=food.price
                )
            )
        Food_selection.objects.bulk_create(selections)

        # clear cart and redirect
        request.session.pop("cart", None)
        messages.success(
            request,
            f"Order #{order.pk} placed! ETA ≈ {order.eta.astimezone().strftime('%H:%M')}."
        )
        return redirect(reverse("order_detail", args=[order.pk]))

class OrderDetailView(DetailView):
  '''Define a show class to show a order object'''
  model = Order
  template_name = "food_rush/order_detail.html"
  context_object_name = "order"

  def get_context_data(self, **kwargs):
     ctx = super().get_context_data(**kwargs)
     ctx["total"] = sum(sel.line_total() for sel in self.object.selections.all())
     return ctx
  
class CreateProfileView(CreateView):
   '''Define a create class to create a profile'''

   form_class = CreateCustomerForm
   template_name = 'food_rush/create_customer_form.html'

   def get_context_data(self, **kwargs):
      '''Method that provides variables to the context'''
      context = super().get_context_data(**kwargs)

      if 'user_form' not in context:
         context['user_form'] = UserCreationForm()
      return context
   
   def form_valid(self,form):
      '''Method to check that the form is valid'''
      user_form = UserCreationForm(self.request.POST)
      if user_form.is_valid():
         
         user = user_form.save()
         login(self.request, user)
         form.instance.user = user

         return super().form_valid(form)
      else:
         return self.form_invalid(form)
      
@require_POST
def clear_cart(request):
   '''Remove the items from the cart and redirect the user back to the cart page'''
   request.session.pop("cart", None)
   messages.success(request, "Your cart has been emptied")
   return redirect(reverse("cart_view"))

class ShowOrderHistoryView(DetailView):
   '''View to show a customers order'''
   model = Customer
   template_name = "food_rush/order_history.html"

   def get_object(self):
      '''Retrieve the Customer of the currently logged-in user'''
      return get_object_or_404(Customer, user=self.request.user)
   
   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    customer = self.request.user.customer
    orders = customer.get_order_history()

  

    context["customer"] = customer
    context["orders"] = orders
    return context