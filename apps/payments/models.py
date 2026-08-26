"""
Payment model — records every Paystack transaction linked to an Order.
The webhook handler updates this record and flips Order.status to 'paid'.
"""

from django.db import models
from apps.orders.models import Order


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        SUCCESS   = 'success',   'Success'
        FAILED    = 'failed',    'Failed'
        ABANDONED = 'abandoned', 'Abandoned'

    order               = models.OneToOneField(Order, on_delete=models.PROTECT, related_name='payment')
    paystack_reference  = models.CharField(max_length=128, unique=True)
    paystack_access_code = models.CharField(max_length=256, blank=True)
    amount              = models.DecimalField(max_digits=10, decimal_places=2)
    currency            = models.CharField(max_length=8, default='GHS')
    status              = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
    )
    channel             = models.CharField(max_length=32, blank=True)   # card / mobile_money etc.
    metadata            = models.JSONField(default=dict, blank=True)
    paid_at             = models.DateTimeField(null=True, blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Payment'
        verbose_name_plural = 'Payments'
        ordering            = ['-created_at']

    def __str__(self):
        return f'{self.paystack_reference} — {self.status}'


PAYSTACK_CURRENCY = 'GHS'          # Ghana Cedis — change to NGN for Nigeria etc.
PAYSTACK_KOBO_MULTIPLIER = 100     # Paystack expects amount in kobo/pesewas (smallest unit)
