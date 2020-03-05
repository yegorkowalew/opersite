from django.contrib import admin

# Register your models here.
from .models import Order


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     pass

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'couterparty', 'order_no', 'in_id')

admin.site.register(Order, OrderAdmin)