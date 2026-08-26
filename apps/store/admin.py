from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display       = ('name', 'is_active', 'created_at', 'image_preview')
    list_filter        = ('is_active',)
    search_fields      = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields    = ('image_preview',)

    def image_preview(self, obj):
        if getattr(obj, 'image_url', None):
            return format_html('<img src="{}" style="max-height: 64px; object-fit: contain;" />', obj.image_url)
        return '-'
    image_preview.short_description = 'Image URL'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display       = ('name', 'category', 'price', 'stock_quantity', 'is_featured', 'is_active', 'image_preview')
    list_filter        = ('category', 'is_featured', 'is_active')
    search_fields      = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable      = ('price', 'stock_quantity', 'is_featured', 'is_active')
    readonly_fields    = ('image_preview',)

    def image_preview(self, obj):
        if getattr(obj, 'image_url', None):
            return format_html('<img src="{}" style="max-height: 64px; object-fit: contain;" />', obj.image_url)
        return '-'
    image_preview.short_description = 'Image URL'
