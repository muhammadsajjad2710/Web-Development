# Awan Rent A Car - Car Rental Service Website

A comprehensive car rental service website offering local rentals in Islamabad and intercity services to major cities in Pakistan.

## Features

- **Vehicle Listings**: Browse cars by category (sedan, SUV, luxury)
- **Local Rentals**: Rent cars in Islamabad
- **Intercity Services**: Travel between major cities
- **Booking System**: Easy online booking with date selection
- **Admin Panel**: Manage vehicles, bookings, and users
- **Responsive Design**: Works on all devices
- **Contact Integration**: WhatsApp, Facebook, and Instagram links

## Intercity Routes

- Islamabad to Lahore
- Islamabad to Karachi
- Islamabad to Peshawar
- Islamabad to Faisalabad
- Islamabad to Sargodha
- Islamabad to Mianwali
- Islamabad to Multan

## Tech Stack

- **Backend**: Django 4.2.7 with Django REST Framework
- **Frontend**: React 18 with Tailwind CSS
- **Database**: MySQL (configured for XAMPP)
- **Authentication**: Django built-in auth system

## Contact Information

- **Phone**: +92-300-0000000
- **Facebook**: facebook.com/AwanRentACar
- **Instagram**: instagram.com/AwanRentACar
- **WhatsApp**: +92-300-0000000

## Setup Instructions

### Backend Setup

1. **Start XAMPP and MySQL Service:**
   - Open XAMPP Control Panel
   - Start Apache and MySQL services
   - Open phpMyAdmin (http://localhost/phpmyadmin)
   - Create a new database named `awan_rental_db`

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   cd backend
   python manage.py migrate
   ```

4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm start
   ```

## Project Structure

```
awan-rent-a-car/
├── backend/                 # Django backend
│   ├── awan_rental/        # Main Django project
│   ├── vehicles/           # Vehicle management app
│   ├── bookings/           # Booking management app
│   └── users/              # User management app
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   └── public/             # Static files
├── requirements.txt         # Python dependencies
├── package.json            # Node.js dependencies
└── README.md               # This file
```

## API Endpoints

- `/api/vehicles/` - Vehicle listings
- `/api/bookings/` - Booking management
- `/api/users/` - User management
- `/api/cities/` - Available cities for intercity travel

## Development

The project uses:
- Django REST Framework for API development
- React Router for frontend routing
- Tailwind CSS for styling
- Framer Motion for animations
- React Hook Form for form handling

## License

This project is for demonstration purposes.
