"""
Store models: Category and Product.
Slugs are auto-generated and unique, used for SEO-friendly URLs.
"""

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name        = models.CharField(max_length=128, unique=True)
    slug        = models.SlugField(max_length=128, unique=True, blank=True)
    description = models.TextField(blank=True)
    image_url   = models.URLField(blank=True)
    image       = models.ImageField(upload_to='categories/', blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name        = 'Category'
        verbose_name_plural = 'Categories'
        ordering            = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category       = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
    )
    name           = models.CharField(max_length=255)
    slug           = models.SlugField(max_length=255, unique=True, blank=True)
    description    = models.TextField()
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    image_url       = models.URLField(blank=True)
    image           = models.ImageField(upload_to='products/', blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_featured    = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
   

    class Meta:
        verbose_name        = 'Product'
        verbose_name_plural = 'Products'
        ordering            = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug      = base_slug
            counter   = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

    @property
    def display_image(self):
        """Returns the uploaded image, URL image, or a placeholder."""
        if self.image:
            return self.image.url

        # Prefer an explicit image URL if provided on the product
        if self.image_url:
            return self.image_url

        # Legacy support for an ImageField named `image` if present
        try:
            if hasattr(self, 'image') and getattr(self.image, 'url', None):
                return self.image.url
        except Exception:
            pass

        # Final fallback to a local SVG placeholder
        return '/static/img/product-placeholder.svg'