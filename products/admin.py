from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'category',
        'price',
        'discount_price',
        'stock',
        'is_available',
        'created_at',
    )
    list_filter = ('is_available', 'category', 'created_at')
    search_fields = ('name', 'sku', 'slug', 'description')
    list_editable = ('stock', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    autocomplete_fields = ('category',)

    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'sku', 'description', 'image'),
        }),
        ('Pricing & inventory', {
            'fields': ('price', 'discount_price', 'stock', 'is_available'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
