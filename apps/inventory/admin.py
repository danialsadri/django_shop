from django.contrib import admin
from .models import StockRecord


@admin.register(StockRecord)
class StockRecordAdmin(admin.ModelAdmin):
    list_display = ['product', 'sku', 'buy_price', 'sale_price', 'num_stock', 'threshold_low_stack']
    search_fields = ['product__title']
    raw_id_fields = ['product']
