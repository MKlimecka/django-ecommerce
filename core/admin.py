from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from store.admin import ProductAdmin, ProductImageInline
from store.models import Product
from tags.models import Tagged_item
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
   add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )
   

class TagInline(GenericTabularInline):
   autocomplete_fields = ['tag']
   model = Tagged_item


class CustomProductAdmin(ProductAdmin):
   inlines= [TagInline, ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
