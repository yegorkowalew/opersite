from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView
from baseorders.models import Order

class OrderList(ListView):
    model = Order

# def start():
#     pass