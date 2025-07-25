from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
from django.db.models import Count


# Register your models here.
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10','Low')
        ]
    
    def queryset(self, request, queryset:QuerySet):
        if self.value()=='<10':
            return queryset.filter(inventory__lt=10)
        

class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img scr="{instance.image.url}" class="thumbnail"/>')
        return ''



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    
    search_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    inlines = [ProductImageInline]
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection','last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return  'OK'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )

    class Media:
        css = {
            'all': ['store/'
            'styles.css']
        }



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


class OrderItemInLine(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    model = models.Order_item

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInLine]
    list_display = ['id', 'placed_at', 'customer']
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def product_count(self, collection):
        url = (
            reverse('admin:store_product_changelist') 
            + '?'
            + urlencode({
                'collection_id': str(collection.id)
            }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count )
        
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    search_fields = ['customer__user__email', 'user__username']
    list_filter = ['user', 'created_at']

# @admin.register(models.Cart_item)
# class Cart_itemAdmin(admin.ModelAdmin):
#     list_display = ['cart', 'product', 'quantity']
#     search_fields = ['product__tittle']
#     list_filter = ['product']


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product']
    search_fields = ['customer__user__email', 'product__title']
    list_filter = ['product']

    