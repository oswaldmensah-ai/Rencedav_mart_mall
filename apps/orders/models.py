from django.db import models
from django.conf import settings
from apps.store.models import Product

class DeliveryArea(models.Model):
    """Stores list of Ghana neighborhoods/towns and their flat shipping rates."""
    name = models.CharField(max_length=100, unique=True) # e.g., "East Legon", "Tema"
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2) # e.g., 40.00

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (GH₵ {self.delivery_fee})"


class Order(models.Model):
    """Stores the customer's core shipping data and payment state."""
    STATUS_CHOICES = [
        ('Pending', 'Pending Payment'),
        ('Paid', 'Paid / Preparing'),
        ('Shipped', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    FULFILLMENT_CHOICES = [
        ('delivery', 'Delivery'),
        ('pickup', 'Pickup'),
    ]
    
    # Links to user profile if logged in; remains null for guest checkouts
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, blank=True, help_text='Customer email address for payment receipt')
    phone_number = models.CharField(max_length=15) # Essential for Mobile Money / Driver contact
    fulfillment_type = models.CharField(max_length=10, choices=FULFILLMENT_CHOICES, default='delivery')
    
    # Kept for backward compatibility with older orders.
    delivery_area = models.ForeignKey(DeliveryArea, on_delete=models.PROTECT, related_name='orders', null=True, blank=True)


    delivery_address = models.TextField(help_text="Exact location and a landmark", blank=True, default='')
    delivery_special_message = models.TextField(
        help_text="Optional message for the package (e.g., leave with receptionist)",
        blank=True,
        default='',
    )

    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    needs_review = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.full_name}"
    
    def get_delivery_fee(self):
        """Return the delivery fee for the selected delivery area."""
        if self.fulfillment_type != 'delivery' or not self.delivery_area:
            return 0
        return float(self.delivery_area.delivery_fee)


class OrderItem(models.Model):
    """A line-item table recording exactly what products were in a specific order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2) # Snapshots price at checkout time
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    def get_cost(self):
        return self.price * self.quantity