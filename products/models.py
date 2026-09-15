from django.core.validators import MinValueValidator
from django.db import models

from core.slug import generate_unique_slug


class Product(models.Model):
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.CASCADE,
        related_name='products',
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=270, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.01)],
    )
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    is_available = models.BooleanField(default=True)
    sku = models.CharField(max_length=100, unique=True, verbose_name='SKU / Product code')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_available']),
            models.Index(fields=['sku']),
        ]

    def __str__(self):
        return self.name

    @property
    def effective_price(self):
        if self.discount_price is not None:
            return self.discount_price
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.name, instance=self)
        super().save(*args, **kwargs)
