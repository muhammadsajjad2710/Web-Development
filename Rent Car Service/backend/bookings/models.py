from django.db import models
from django.conf import settings
from vehicles.models import Vehicle, City


class Booking(models.Model):
    BOOKING_TYPE_CHOICES = [
        ('local', 'Local Rental'),
        ('intercity', 'Intercity Trip'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPE_CHOICES)
    
    # Local rental fields
    pickup_date = models.DateTimeField()
    return_date = models.DateTimeField()
    
    # Intercity trip fields
    destination_city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True, related_name='bookings')
    departure_date = models.DateTimeField(blank=True, null=True)
    return_date_intercity = models.DateTimeField(blank=True, null=True)
    
    # Common fields
    pickup_location = models.CharField(max_length=200, default='Islamabad')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.vehicle.name}"
    
    class Meta:
        ordering = ['-created_at']


class BookingPayment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Payment'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for Booking {self.booking.id}"
    
    class Meta:
        verbose_name = 'Booking Payment'
        verbose_name_plural = 'Booking Payments'
