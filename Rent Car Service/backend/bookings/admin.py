from django.contrib import admin
from .models import Booking, BookingPayment


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'vehicle', 'booking_type', 'status', 'total_amount', 'created_at']
    list_filter = ['booking_type', 'status', 'created_at', 'pickup_date']
    search_fields = ['user__username', 'user__email', 'vehicle__name', 'vehicle__brand']
    list_editable = ['status']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'vehicle', 'booking_type', 'status')
        }),
        ('Local Rental Details', {
            'fields': ('pickup_date', 'return_date'),
            'classes': ('collapse',)
        }),
        ('Intercity Trip Details', {
            'fields': ('destination_city', 'departure_date', 'return_date_intercity'),
            'classes': ('collapse',)
        }),
        ('General Information', {
            'fields': ('pickup_location', 'total_amount', 'special_requests')
        }),
    )


@admin.register(BookingPayment)
class BookingPaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'payment_method', 'payment_status', 'payment_date', 'created_at']
    list_filter = ['payment_status', 'payment_method', 'created_at']
    search_fields = ['booking__id', 'transaction_id']
    list_editable = ['payment_status']
    ordering = ['-created_at']
