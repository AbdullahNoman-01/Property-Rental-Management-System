from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'owner',
        'property_type',
        'monthly_rent',
        'bedrooms',
        'bathrooms',
        'availability_status',
        'created_at',
    )

    list_filter = (
        'property_type',
        'availability_status',
    )

    search_fields = (
        'title',
        'location',
        'owner__username',
    )