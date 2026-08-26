from django import forms

from apps.store.models import Category, Product


class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ('name', 'description', 'image_url', 'image', 'is_active')
		widgets = {
			'name': forms.TextInput(attrs={'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm'}),
			'description': forms.Textarea(attrs={'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm', 'rows': 3}),
			'image_url': forms.URLInput(attrs={'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm'}),
			'image': forms.ClearableFileInput(attrs={'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm', 'accept': 'image/*'}),
			'is_active': forms.CheckboxInput(attrs={'class': 'h-4 w-4'}),
		}

	def clean_image(self):
		image = self.cleaned_data.get('image')
		if image and image.size > 5 * 1024 * 1024:
			raise forms.ValidationError('Image files must be 5 MB or smaller.')
		return image


class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = (
			'category',
			'name',
			'description',
			'price',
			'image_url',
			'image',
			'stock_quantity',
			'is_featured',
			'is_active',
		)
		widgets = {
			'category': forms.Select(attrs={'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm'}),
			'name': forms.TextInput(attrs={'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm'}),
			'description': forms.Textarea(attrs={'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm', 'rows': 4}),
			'price': forms.NumberInput(attrs={'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm', 'step': '0.01', 'min': '0'}),
			'image_url': forms.URLInput(attrs={'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm'}),
			'image': forms.ClearableFileInput(attrs={'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm', 'accept': 'image/*'}),
			'stock_quantity': forms.NumberInput(attrs={'class': 'w-full rounded-lg border-stone-300 p-2.5 text-sm', 'min': '0'}),
			'is_featured': forms.CheckboxInput(attrs={'class': 'h-4 w-4'}),
			'is_active': forms.CheckboxInput(attrs={'class': 'h-4 w-4'}),
		}

	def clean_image(self):
		image = self.cleaned_data.get('image')
		if image and image.size > 5 * 1024 * 1024:
			raise forms.ValidationError('Image files must be 5 MB or smaller.')
		return image
