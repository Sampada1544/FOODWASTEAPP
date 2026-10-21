from django.contrib import admin

from .models import FoodDonation, FoodRequest


@admin.register(FoodDonation)
class FoodDonationAdmin(admin.ModelAdmin):

    list_display = (
        'food_name',
        'food_type',
        'quantity',
        'distance_km',
        'donor',
        'priority',
        'status',
        'preparation_date',
        'expiry_date',
        'created_at'
    )

    list_filter = (
        'status',
        'priority',
        'food_type'
    )

    search_fields = (
        'food_name',
        'donor__username',
        'pickup_address'
    )

    ordering = (
        '-created_at',
    )


@admin.register(FoodRequest)
class FoodRequestAdmin(admin.ModelAdmin):

    list_display = (
        'donation',
        'ngo',
        'status',
        'requested_at'
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'donation__food_name',
        'ngo__username'
    )

    ordering = (
        '-requested_at',
    )