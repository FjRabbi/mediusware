from django.contrib import admin
from .models import Product, ProductVariant, ProductImage, Variant, ProductVariantPrice
# Register your models here.

admin.site.register((ProductVariantPrice, Variant, ProductImage, Product, ProductVariant))
