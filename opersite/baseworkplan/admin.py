from django.contrib import admin

from .models import BaseWorkplan

# @admin.register(BaseWorkplan)
# class BaseWorkplanAdmin(admin.ModelAdmin):
#     pass

class BaseWorkplanAdmin(admin.ModelAdmin):
    list_display = ('in_id','letter','shop','start_date','end_date')

admin.site.register(BaseWorkplan, BaseWorkplanAdmin)