from django.db import models


class VehicleCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For FontAwesome icons
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Vehicle Categories'


class Vehicle(models.Model):
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]
    
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model_year = models.IntegerField()
    category = models.ForeignKey(VehicleCategory, on_delete=models.CASCADE, related_name='vehicles')
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    seats = models.IntegerField()
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    weekly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    description = models.TextField()
    features = models.JSONField(default=list, blank=True)  # List of features
    is_available = models.BooleanField(default=True)
    mileage = models.IntegerField(help_text='Current mileage in kilometers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.brand} {self.name} ({self.model_year})"
    
    class Meta:
        ordering = ['-created_at']


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    distance_from_islamabad = models.IntegerField(help_text='Distance in kilometers')
    travel_time = models.IntegerField(help_text='Travel time in minutes')
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ['distance_from_islamabad']
