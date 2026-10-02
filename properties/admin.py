from django.contrib import admin
from .models import Property, RentalRequest, Review

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'price', 'created_at')
    search_fields = ('title', 'address')
    list_filter = ('created_at',)

@admin.register(RentalRequest)
class RentalRequestAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant', 'status', 'created_at')
    list_filter = ('status', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'rating', 'created_at')
    list_filter = ('rating',)