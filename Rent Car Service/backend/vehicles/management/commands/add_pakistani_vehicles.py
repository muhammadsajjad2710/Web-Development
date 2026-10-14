from django.core.management.base import BaseCommand
from vehicles.models import VehicleCategory, Vehicle, City
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Add popular Pakistani vehicles to the database'

    def handle(self, *args, **options):
        self.stdout.write('Adding popular Pakistani vehicles...')

        # Get or create categories
        sedan, _ = VehicleCategory.objects.get_or_create(name='Sedan')
        suv, _ = VehicleCategory.objects.get_or_create(name='SUV')
        luxury, _ = VehicleCategory.objects.get_or_create(name='Luxury')
        hatchback, _ = VehicleCategory.objects.get_or_create(name='Hatchback')
        pickup, _ = VehicleCategory.objects.get_or_create(name='Pickup')

        # Get or create cities
        islamabad, _ = City.objects.get_or_create(
            name='Islamabad',
            defaults={
                'distance_from_islamabad': 0,
                'travel_time': 0,
                'description': 'Capital city of Pakistan'
            }
        )

        # Pakistani Vehicles Data - Updated to match Vehicle model
        pakistani_vehicles = [
            # Suzuki Vehicles (Most Popular in Pakistan)
            {
                'brand': 'Suzuki',
                'name': 'Mehran',
                'category': hatchback,
                'model_year': 2020,
                'fuel_type': 'petrol',
                'transmission': 'manual',
                'seats': 5,
                'daily_rate': 2500,
                'weekly_rate': 15000,
                'monthly_rate': 60000,
                'mileage': 25000,
                'is_available': True,
                'features': ['Air Conditioning', 'Power Steering', 'CD Player', 'Central Locking'],
                'description': 'The iconic Suzuki Mehran, a reliable and fuel-efficient hatchback perfect for city driving.'
            },
            {
                'brand': 'Suzuki',
                'name': 'Cultus',
                'category': hatchback,
                'model_year': 2021,
                'fuel_type': 'petrol',
                'transmission': 'manual',
                'seats': 5,
                'daily_rate': 3000,
                'weekly_rate': 18000,
                'monthly_rate': 72000,
                'mileage': 20000,
                'is_available': True,
                'features': ['Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags'],
                'description': 'Modern Suzuki Cultus with enhanced safety features and comfortable interior.'
            },
            {
                'brand': 'Suzuki',
                'name': 'Swift',
                'category': hatchback,
                'model_year': 2022,
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 4000,
                'weekly_rate': 24000,
                'monthly_rate': 96000,
                'mileage': 15000,
                'is_available': True,
                'features': ['Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags', 'Touchscreen'],
                'description': 'Sporty Suzuki Swift with automatic transmission and modern features.'
            },
            {
                'brand': 'Suzuki',
                'name': 'Alto',
                'category': hatchback,
                'model_year': 2021,
                'fuel_type': 'petrol',
                'transmission': 'manual',
                'seats': 5,
                'daily_rate': 2800,
                'weekly_rate': 16800,
                'monthly_rate': 67200,
                'mileage': 22000,
                'is_available': True,
                'features': ['Air Conditioning', 'Power Steering', 'CD Player'],
                'description': 'Compact Suzuki Alto, perfect for small families and city commuting.'
            },

            # Toyota Vehicles
            {
                'brand': 'Toyota',
                'name': 'Corolla XLI',
                'category': sedan,
                'model_year': 2021,
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 6000,
                'weekly_rate': 36000,
                'monthly_rate': 144000,
                'mileage': 18000,
                'is_available': True,
                'features': ['Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags', 'Touchscreen', 'Reverse Camera'],
                'description': 'Reliable Toyota Corolla XLI with automatic transmission and premium features.'
            },
            {
                'brand': 'Toyota',
                'name': 'Corolla Altis',
                'category': sedan,
                'model_year': 2022,
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 7000,
                'weekly_rate': 42000,
                'monthly_rate': 168000,
                'mileage': 12000,
                'is_available': True,
                'features': ['Dual Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags', 'Touchscreen', 'Reverse Camera', 'Cruise Control'],
                'description': 'Premium Toyota Corolla Altis with luxury features and superior comfort.'
            },
            {
                'brand': 'Toyota',
                'name': 'Fortuner',
                'category': suv,
                'model_year': 2021,
                'fuel_type': 'diesel',
                'transmission': 'automatic',
                'seats': 7,
                'daily_rate': 12000,
                'weekly_rate': 72000,
                'monthly_rate': 288000,
                'mileage': 25000,
                'is_available': True,
                'features': ['Dual Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags', 'Touchscreen', 'Reverse Camera', '4WD', 'Leather Seats'],
                'description': 'Powerful Toyota Fortuner SUV perfect for family trips and off-road adventures.'
            },
            {
                'brand': 'Toyota',
                'name': 'Hilux',
                'category': pickup,
                'model_year': 2020,
                'fuel_type': 'diesel',
                'transmission': 'manual',
                'seats': 5,
                'daily_rate': 8000,
                'weekly_rate': 48000,
                'monthly_rate': 192000,
                'mileage': 35000,
                'is_available': True,
                'features': ['Air Conditioning', 'Power Steering', 'ABS', 'Airbags', '4WD', 'Towing Capacity'],
                'description': 'Robust Toyota Hilux pickup truck for commercial and heavy-duty use.'
            },

            # Honda Vehicles
            {
                'brand': 'Honda',
                'name': 'City',
                'category': sedan,
                'model_year': 2021,
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 6500,
                'weekly_rate': 39000,
                'monthly_rate': 156000,
                'mileage': 20000,
                'is_available': True,
                'features': ['Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags', 'Touchscreen', 'Reverse Camera'],
                'description': 'Elegant Honda City with smooth automatic transmission and premium interior.'
            },
            {
                'brand': 'Honda',
                'name': 'Civic',
                'category': sedan,
                'model_year': 2022,
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 8000,
                'weekly_rate': 48000,
                'monthly_rate': 192000,
                'mileage': 15000,
                'is_available': True,
                'features': ['Dual Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags', 'Touchscreen', 'Reverse Camera', 'Sunroof'],
                'description': 'Sporty Honda Civic with modern design and advanced technology features.'
            },
            {
                'brand': 'Honda',
                'name': 'BR-V',
                'category': suv,
                'model_year': 2021,
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 7,
                'daily_rate': 9000,
                'weekly_rate': 54000,
                'monthly_rate': 216000,
                'mileage': 22000,
                'is_available': True,
                'features': ['Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags', 'Touchscreen', 'Reverse Camera', '7 Seater'],
                'description': 'Spacious Honda BR-V SUV with 7-seater capacity for family trips.'
            },

            # Daihatsu Vehicles
            {
                'brand': 'Daihatsu',
                'name': 'Cuore',
                'category': hatchback,
                'model_year': 2020,
                'fuel_type': 'petrol',
                'transmission': 'manual',
                'seats': 5,
                'daily_rate': 2200,
                'weekly_rate': 13200,
                'monthly_rate': 52800,
                'mileage': 30000,
                'is_available': True,
                'features': ['Air Conditioning', 'Power Steering'],
                'description': 'Compact Daihatsu Cuore, ideal for city driving and parking.'
            },

            # Nissan Vehicles
            {
                'brand': 'Nissan',
                'name': 'Dayz',
                'category': hatchback,
                'model_year': 2021,
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 3500,
                'weekly_rate': 21000,
                'monthly_rate': 84000,
                'mileage': 18000,
                'is_available': True,
                'features': ['Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags'],
                'description': 'Modern Nissan Dayz with automatic transmission and safety features.'
            },

            # Mercedes-Benz (Luxury)
            {
                'brand': 'Mercedes-Benz',
                'name': 'C-Class',
                'category': luxury,
                'model_year': 2021,
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 15000,
                'weekly_rate': 90000,
                'monthly_rate': 360000,
                'mileage': 12000,
                'is_available': True,
                'features': ['Dual Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags', 'Touchscreen', 'Reverse Camera', 'Leather Seats', 'Panoramic Sunroof'],
                'description': 'Luxurious Mercedes-Benz C-Class with premium features and superior comfort.'
            },
            {
                'brand': 'Mercedes-Benz',
                'name': 'E-Class',
                'category': luxury,
                'model_year': 2022,
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 20000,
                'weekly_rate': 120000,
                'monthly_rate': 480000,
                'mileage': 8000,
                'is_available': True,
                'features': ['Dual Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags', 'Touchscreen', 'Reverse Camera', 'Leather Seats', 'Panoramic Sunroof', 'Massage Seats'],
                'description': 'Executive Mercedes-Benz E-Class with ultimate luxury and comfort features.'
            },

            # BMW (Luxury)
            {
                'brand': 'BMW',
                'name': '3 Series',
                'category': luxury,
                'model_year': 2021,
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 18000,
                'weekly_rate': 108000,
                'monthly_rate': 432000,
                'mileage': 15000,
                'is_available': True,
                'features': ['Dual Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags', 'Touchscreen', 'Reverse Camera', 'Leather Seats', 'Sport Mode'],
                'description': 'Sporty BMW 3 Series with dynamic driving experience and luxury features.'
            },
            {
                'brand': 'BMW',
                'name': '5 Series',
                'category': luxury,
                'model_year': 2022,
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 25000,
                'weekly_rate': 150000,
                'monthly_rate': 600000,
                'mileage': 10000,
                'is_available': True,
                'features': ['Dual Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags', 'Touchscreen', 'Reverse Camera', 'Leather Seats', 'Panoramic Sunroof', 'Heated Seats'],
                'description': 'Premium BMW 5 Series with executive luxury and advanced technology.'
            },

            # Hyundai Vehicles
            {
                'brand': 'Hyundai',
                'name': 'i10',
                'category': hatchback,
                'model_year': 2021,
                'fuel_type': 'petrol',
                'transmission': 'manual',
                'seats': 5,
                'daily_rate': 3200,
                'weekly_rate': 19200,
                'monthly_rate': 76800,
                'mileage': 22000,
                'is_available': True,
                'features': ['Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags'],
                'description': 'Modern Hyundai i10 with contemporary design and good fuel efficiency.'
            },
            {
                'brand': 'Hyundai',
                'name': 'Elantra',
                'category': sedan,
                'model_year': 2022,
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 7500,
                'weekly_rate': 45000,
                'monthly_rate': 180000,
                'mileage': 12000,
                'is_available': True,
                'features': ['Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags', 'Touchscreen', 'Reverse Camera', 'Sunroof'],
                'description': 'Stylish Hyundai Elantra with modern features and comfortable interior.'
            },

            # Kia Vehicles
            {
                'brand': 'Kia',
                'name': 'Sportage',
                'category': suv,
                'model_year': 2021,
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 10000,
                'weekly_rate': 60000,
                'monthly_rate': 240000,
                'mileage': 20000,
                'is_available': True,
                'features': ['Dual Air Conditioning', 'Power Steering', 'Power Windows', 'ABS', 'Airbags', 'Touchscreen', 'Reverse Camera', '4WD'],
                'description': 'Modern Kia Sportage SUV with contemporary design and advanced features.'
            }
        ]

        # Create vehicles
        vehicles_created = 0
        for vehicle_data in pakistani_vehicles:
            vehicle, created = Vehicle.objects.get_or_create(
                brand=vehicle_data['brand'],
                name=vehicle_data['name'],
                model_year=vehicle_data['model_year'],
                defaults=vehicle_data
            )
            if created:
                vehicles_created += 1
                self.stdout.write(f'Created: {vehicle.brand} {vehicle.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added {vehicles_created} new Pakistani vehicles!'
            )
        )
