from django.contrib import admin
from .models import Product, Sale

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'quantity_in_stock', 'price')
    search_fields = ('name', 'sku')
    list_filter = ('category',)
    ordering = ('name',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_sold', 'sale_date')
    search_fields = ('product__name',)
    date_hierarchy = 'sale_date'
