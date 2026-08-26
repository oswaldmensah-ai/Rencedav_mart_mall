from django.contrib import admin
from .models import Order, OrderItem, DeliveryArea

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # Cleaned up mismatched fields to prevent system check errors
    fields = ['product', 'quantity']
    readonly_fields = ['product', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'fulfillment_type', 'status', 'total_amount', 'created_at']
    list_filter = ['fulfillment_type', 'status', 'created_at']
    readonly_fields = ['created_at']
    search_fields = ['full_name', 'email', 'phone_number']
    inlines = [OrderItemInline]


