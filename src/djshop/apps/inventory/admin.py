from django.contrib import admin
from djshop.apps.inventory.models import StockRecord


@admin.register(StockRecord)
class StockRecordAdmin(admin.ModelAdmin):
    pass
