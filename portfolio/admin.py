from django.contrib import admin
from .models import Stock

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'quantity', 'purchase_price', 'purchase_date')

from .models import Note

admin.site.register(Note)