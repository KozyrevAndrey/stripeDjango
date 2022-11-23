from django.contrib import admin

# Register your models here.
from payments.models import Item


class ItemAdm(admin.ModelAdmin):
    list_display = [
        'name', 'description', 'price'
    ]
    list_display_links = ['name']
    search_fields = ['name', 'description', 'price', 'stripe_product_id', 'stripe_price_id']
    list_filter = ['price']
    list_per_page = 20
    list_max_show_all = 50


admin.site.register(Item, ItemAdm)