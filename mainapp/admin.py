from django.contrib import admin

from .models import *


class InlineImage(admin.TabularInline):
    model = Image


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        InlineImage,
               ]


admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)

