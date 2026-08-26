from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display   = ('paystack_reference', 'order', 'amount', 'currency', 'status', 'paid_at')
    list_filter    = ('status', 'currency')
    search_fields  = ('paystack_reference', 'order__id', 'order__full_name')
    readonly_fields = ('paystack_reference', 'paystack_access_code', 'metadata', 'created_at')
