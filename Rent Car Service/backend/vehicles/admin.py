from django.contrib import admin
from .models import Vehicle, VehicleCategory, City


@admin.register(VehicleCategory)
class VehicleCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'fuel_type', 'transmission', 'daily_rate', 'is_available']
    list_filter = ['category', 'fuel_type', 'transmission', 'is_available', 'model_year']
    search_fields = ['name', 'brand', 'description']
    list_editable = ['is_available', 'daily_rate']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'brand', 'model_year', 'category', 'description')
        }),
        ('Specifications', {
            'fields': ('fuel_type', 'transmission', 'seats', 'mileage', 'features')
        }),
        ('Pricing', {
            'fields': ('daily_rate', 'weekly_rate', 'monthly_rate')
        }),
        ('Status', {
            'fields': ('is_available', 'image')
        }),
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'distance_from_islamabad', 'travel_time']
    list_filter = ['distance_from_islamabad']
    search_fields = ['name']
    ordering = ['distance_from_islamabad']
