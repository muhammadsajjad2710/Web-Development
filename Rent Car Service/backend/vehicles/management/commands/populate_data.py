from django.core.management.base import BaseCommand
from vehicles.models import VehicleCategory, Vehicle, City
from users.models import CustomUser
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Populate database with sample data for Awan Rent A Car'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create vehicle categories
        categories = [
            {'name': 'Sedan', 'description': 'Comfortable and fuel-efficient sedans for daily use'},
            {'name': 'SUV', 'description': 'Spacious SUVs perfect for family trips and off-road adventures'},
            {'name': 'Luxury', 'description': 'Premium luxury vehicles for special occasions'},
            {'name': 'Hatchback', 'description': 'Compact and economical hatchbacks for city driving'}
        ]

        for cat_data in categories:
            category, created = VehicleCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create cities
        cities = [
            {'name': 'Lahore', 'distance_from_islamabad': 280, 'travel_time': 210, 'description': 'Cultural capital of Pakistan'},
            {'name': 'Karachi', 'distance_from_islamabad': 1200, 'travel_time': 960, 'description': 'Port city and economic hub'},
            {'name': 'Peshawar', 'distance_from_islamabad': 180, 'travel_time': 150, 'description': 'Gateway to Khyber Pass'},
            {'name': 'Faisalabad', 'distance_from_islamabad': 320, 'travel_time': 240, 'description': 'Textile city of Pakistan'},
            {'name': 'Sargodha', 'distance_from_islamabad': 200, 'travel_time': 150, 'description': 'Orange city of Pakistan'},
            {'name': 'Mianwali', 'distance_from_islamabad': 150, 'travel_time': 120, 'description': 'Historical city in Punjab'},
            {'name': 'Multan', 'distance_from_islamabad': 400, 'travel_time': 300, 'description': 'City of Saints'}
        ]

        for city_data in cities:
            city, created = City.objects.get_or_create(
                name=city_data['name'],
                defaults=city_data
            )
            if created:
                self.stdout.write(f'Created city: {city.name}')

        # Create sample vehicles
        vehicles = [
            {
                'name': 'Toyota Corolla',
                'brand': 'Toyota',
                'model_year': 2022,
                'category': 'Sedan',
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 5000,
                'weekly_rate': 30000,
                'monthly_rate': 120000,
                'description': 'Reliable and fuel-efficient sedan perfect for daily commuting and city driving.',
                'features': ['Air Conditioning', 'Power Steering', 'Bluetooth', 'Backup Camera'],
                'mileage': 15000
            },
            {
                'name': 'Honda City',
                'brand': 'Honda',
                'model_year': 2021,
                'category': 'Sedan',
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 4500,
                'weekly_rate': 27000,
                'monthly_rate': 108000,
                'description': 'Comfortable sedan with excellent fuel economy and modern features.',
                'features': ['Air Conditioning', 'Power Windows', 'USB Charging', 'ABS'],
                'mileage': 25000
            },
            {
                'name': 'Toyota Fortuner',
                'brand': 'Toyota',
                'model_year': 2023,
                'category': 'SUV',
                'fuel_type': 'diesel',
                'transmission': 'automatic',
                'seats': 7,
                'daily_rate': 8000,
                'weekly_rate': 48000,
                'monthly_rate': 192000,
                'description': 'Premium SUV with powerful engine and spacious interior for family trips.',
                'features': ['4WD', 'Leather Seats', 'Navigation', 'Sunroof', 'Third Row Seating'],
                'mileage': 8000
            },
            {
                'name': 'Honda BR-V',
                'brand': 'Honda',
                'model_year': 2022,
                'category': 'SUV',
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 7,
                'daily_rate': 6000,
                'weekly_rate': 36000,
                'monthly_rate': 144000,
                'description': 'Compact SUV with excellent fuel efficiency and versatile seating.',
                'features': ['Air Conditioning', 'Power Steering', 'Bluetooth', 'Backup Camera'],
                'mileage': 18000
            },
            {
                'name': 'Mercedes-Benz C-Class',
                'brand': 'Mercedes-Benz',
                'model_year': 2023,
                'category': 'Luxury',
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 15000,
                'weekly_rate': 90000,
                'monthly_rate': 360000,
                'description': 'Luxury sedan with premium features and elegant design for special occasions.',
                'features': ['Leather Seats', 'Navigation', 'Premium Audio', 'Panoramic Sunroof', 'Heated Seats'],
                'mileage': 5000
            },
            {
                'name': 'BMW 3 Series',
                'brand': 'BMW',
                'model_year': 2022,
                'category': 'Luxury',
                'fuel_type': 'petrol',
                'transmission': 'automatic',
                'seats': 5,
                'daily_rate': 14000,
                'weekly_rate': 84000,
                'monthly_rate': 336000,
                'description': 'Sporty luxury sedan with dynamic performance and sophisticated technology.',
                'features': ['Sport Seats', 'Navigation', 'Premium Audio', 'LED Headlights', 'Sport Package'],
                'mileage': 12000
            },
            {
                'name': 'Suzuki Swift',
                'brand': 'Suzuki',
                'model_year': 2021,
                'category': 'Hatchback',
                'fuel_type': 'petrol',
                'transmission': 'manual',
                'seats': 5,
                'daily_rate': 3000,
                'weekly_rate': 18000,
                'monthly_rate': 72000,
                'description': 'Compact hatchback perfect for city driving and parking.',
                'features': ['Air Conditioning', 'Power Steering', 'Fuel Efficient', 'Easy Parking'],
                'mileage': 30000
            }
        ]

        for vehicle_data in vehicles:
            category = VehicleCategory.objects.get(name=vehicle_data['category'])
            vehicle, created = Vehicle.objects.get_or_create(
                name=vehicle_data['name'],
                brand=vehicle_data['brand'],
                model_year=vehicle_data['model_year'],
                defaults={
                    'category': category,
                    'fuel_type': vehicle_data['fuel_type'],
                    'transmission': vehicle_data['transmission'],
                    'seats': vehicle_data['seats'],
                    'daily_rate': vehicle_data['daily_rate'],
                    'weekly_rate': vehicle_data['weekly_rate'],
                    'monthly_rate': vehicle_data['monthly_rate'],
                    'description': vehicle_data['description'],
                    'features': vehicle_data['features'],
                    'mileage': vehicle_data['mileage']
                }
            )
            if created:
                self.stdout.write(f'Created vehicle: {vehicle.brand} {vehicle.name}')

        # Create a sample admin user
        admin_user, created = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@awanrentacar.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
                'password': make_password('admin123')
            }
        )
        if created:
            self.stdout.write('Created admin user: admin (password: admin123)')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
