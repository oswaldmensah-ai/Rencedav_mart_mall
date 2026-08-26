from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        # Order model does not include customer_latitude/customer_longitude.
        fields = ['full_name', 'email', 'phone_number', 'fulfillment_type', 'delivery_address', 'delivery_special_message']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm', 'placeholder': 'Kofi Mensah'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm', 'placeholder': '0241234567'}),
            'fulfillment_type': forms.RadioSelect(attrs={'class': 'fulfillment-type-radio'}),
            'delivery_address': forms.Textarea(
                attrs={
                    'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm',
                    'rows': 3,
                    'placeholder': 'Apt 4B, near the container spot, close to the school gate.',
                }
            ),
            'delivery_special_message': forms.Textarea(
                attrs={
                    'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm',
                    'rows': 3,
                    'placeholder': 'Leave with the receptionist / Call on arrival',
                }
            ),
        }


    
    def clean(self):
        cleaned_data = super().clean()
        fulfillment_type = cleaned_data.get('fulfillment_type')
        delivery_address = cleaned_data.get('delivery_address')

        if fulfillment_type == 'delivery':
            if not delivery_address or delivery_address.strip() == '':
                raise forms.ValidationError('Delivery address (including landmark) is required for delivery orders.')

        return cleaned_data

