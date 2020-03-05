from django.contrib import admin

from .models import ShipmentDates, PickupDates, DesignDates, ServiceNoteDates

# @admin.register(ShipmentDates)
# class ShipmentDatesAdmin(admin.ModelAdmin):
#     pass
class ShipmentDatesAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'in_id', 'shipment_plan_start_date', 'shipment_plan_end_date', 'shipment_fact_end_date', 'shipment_need', 'shipment_dispatcher')

# @admin.register(PickupDates)
# class PickupDatesAdmin(admin.ModelAdmin):
#     pass
class PickupDatesAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'in_id', 'pickup_plan_start_date', 'pickup_plan_end_date', 'pickup_fact_end_date', 'pickup_need', 'pickup_dispatcher')


# @admin.register(DesignDates)
# class DesignDatesAdmin(admin.ModelAdmin):
#     pass
class DesignDatesAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'in_id', 'design_plan_start_date', 'design_plan_end_date', 'design_fact_end_date', 'design_need', 'design_dispatcher')


# @admin.register(ServiceNoteDates)
# class ServiceNoteDatesAdmin(admin.ModelAdmin):
#     pass

class ServiceNoteDatesAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'in_id', 'sn_plan_start_date', 'sn_plan_end_date', 'sn_fact_end_date', 'sn_need', 'sn_dispatcher')

admin.site.register(ServiceNoteDates, ServiceNoteDatesAdmin)
admin.site.register(DesignDates, DesignDatesAdmin)
admin.site.register(PickupDates, PickupDatesAdmin)
admin.site.register(ShipmentDates, ShipmentDatesAdmin)