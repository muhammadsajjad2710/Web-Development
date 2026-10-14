# Awan Rent A Car - Project Structure

This document outlines the complete structure of the Awan Rent A Car project, including both the Django backend and React frontend.

## 📁 Root Directory Structure

```
awan-rent-a-car/
├── backend/                 # Django backend application
├── frontend/               # React frontend application
├── requirements.txt         # Python dependencies
├── package.json            # Node.js dependencies
├── setup.py                # Automated setup script
├── README.md               # Project documentation
└── PROJECT_STRUCTURE.md    # This file
```

## 🐍 Backend (Django) Structure

### Main Project
```
backend/
├── awan_rental/            # Main Django project
│   ├── __init__.py
│   ├── settings.py         # Django settings with MySQL configuration
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── manage.py               # Django management script
├── requirements.txt         # Python dependencies
└── media/                  # Media files (vehicle images)
```

### Django Apps

#### Users App
```
backend/users/
├── __init__.py
├── apps.py                 # App configuration
├── models.py               # CustomUser model
├── admin.py                # Admin interface configuration
├── serializers.py          # API serializers
├── views.py                # API views (login, register, profile)
└── urls.py                 # URL patterns
```

#### Vehicles App
```
backend/vehicles/
├── __init__.py
├── apps.py                 # App configuration
├── models.py               # Vehicle, VehicleCategory, City models
├── admin.py                # Admin interface configuration
├── serializers.py          # API serializers
├── views.py                # API views (CRUD operations)
├── urls.py                 # URL patterns
└── management/             # Django management commands
    └── commands/
        └── populate_data.py # Sample data population
```

#### Bookings App
```
backend/bookings/
├── __init__.py
├── apps.py                 # App configuration
├── models.py               # Booking and BookingPayment models
├── admin.py                # Admin interface configuration
├── serializers.py          # API serializers
├── views.py                # API views (booking management)
└── urls.py                 # URL patterns
```

## ⚛️ Frontend (React) Structure

### Main Application
```
frontend/
├── public/
│   └── index.html          # Main HTML file
├── src/
│   ├── App.js              # Main React component with routing
│   ├── App.css             # Main CSS with Tailwind imports
│   ├── index.js            # React entry point
│   ├── index.css           # Base CSS
│   ├── contexts/           # React contexts
│   │   └── AuthContext.js  # Authentication context
│   ├── components/         # Reusable components
│   │   ├── Navbar.js       # Navigation component
│   │   └── Footer.js       # Footer component
│   └── pages/              # Page components
│       ├── Home.js         # Home page
│       ├── Contact.js      # Contact page
│       ├── Login.js        # Login page (to be created)
│       ├── Register.js     # Register page (to be created)
│       ├── Vehicles.js     # Vehicle listings (to be created)
│       ├── VehicleDetail.js # Vehicle details (to be created)
│       ├── Booking.js      # Booking form (to be created)
│       ├── Profile.js      # User profile (to be created)
│       └── MyBookings.js   # User bookings (to be created)
├── package.json            # Node.js dependencies
├── tailwind.config.js      # Tailwind CSS configuration
└── postcss.config.js       # PostCSS configuration
```

## 🗄️ Database Models

### Users
- **CustomUser**: Extended user model with phone, address, and verification status

### Vehicles
- **VehicleCategory**: Vehicle categories (Sedan, SUV, Luxury, Hatchback)
- **Vehicle**: Vehicle details with specifications, pricing, and availability
- **City**: Intercity destinations with distance and travel time

### Bookings
- **Booking**: Booking records for local rentals and intercity trips
- **BookingPayment**: Payment information for bookings

## 🔌 API Endpoints

### Authentication
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `POST /api/users/logout/` - User logout
- `GET /api/users/profile/` - Get user profile
- `PATCH /api/users/profile/` - Update user profile

### Vehicles
- `GET /api/vehicles/` - List all vehicles
- `GET /api/vehicles/<id>/` - Get vehicle details
- `GET /api/categories/` - List vehicle categories
- `GET /api/cities/` - List intercity destinations

### Bookings
- `GET /api/bookings/` - List user bookings
- `POST /api/bookings/create/` - Create new booking
- `GET /api/bookings/<id>/` - Get booking details
- `PATCH /api/bookings/<id>/update/` - Update booking
- `PATCH /api/bookings/<id>/cancel/` - Cancel booking

## 🎨 Frontend Features

### Components
- **Responsive Navigation**: Mobile-friendly navigation with authentication state
- **Hero Sections**: Attractive landing pages with call-to-action buttons
- **Contact Forms**: Interactive contact forms with validation
- **Social Media Integration**: Links to Facebook, Instagram, and WhatsApp

### Pages
- **Home**: Company overview, features, testimonials, and intercity routes
- **Contact**: Contact form, company information, and social media links
- **Vehicles**: Vehicle listings with filtering and search (to be implemented)
- **Booking**: Online booking system (to be implemented)
- **Authentication**: Login and registration pages (to be implemented)

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- XAMPP (for MySQL database)
- Git

### Quick Setup
1. **Clone the repository**
2. **Run the setup script**: `python setup.py`
3. **Start XAMPP** and create database `awan_rental_db`
4. **Backend setup**:
   - Navigate to `backend/`
   - Activate virtual environment
   - Run migrations: `python manage.py migrate`
   - Populate data: `python manage.py populate_data`
   - Start server: `python manage.py runserver`
5. **Frontend setup**:
   - Navigate to `frontend/`
   - Start app: `npm start`

## 🔧 Configuration

### Database
- **Engine**: MySQL (configured for XAMPP)
- **Database**: `awan_rental_db`
- **User**: `root`
- **Password**: (empty)
- **Host**: `localhost`
- **Port**: `3306`

### CORS Settings
- Allowed origins: `http://localhost:3000`, `http://127.0.0.1:3000`
- Credentials: Enabled

### Static Files
- **Backend**: `/static/` and `/media/`
- **Frontend**: Built with Create React App

## 📱 Features

### Vehicle Management
- Vehicle categories and specifications
- Pricing (daily, weekly, monthly rates)
- Image uploads and feature lists
- Availability status

### Booking System
- Local rentals in Islamabad
- Intercity travel to major cities
- Date selection and pricing calculation
- Payment tracking

### User Management
- User registration and authentication
- Profile management
- Booking history
- Admin panel access

### Intercity Routes
- Islamabad to Lahore (280 km)
- Islamabad to Karachi (1,200 km)
- Islamabad to Peshawar (180 km)
- Islamabad to Faisalabad (320 km)
- Islamabad to Sargodha (200 km)
- Islamabad to Mianwali (150 km)
- Islamabad to Multan (400 km)

## 🎯 Next Steps

### To Complete the Project
1. **Implement remaining React pages**:
   - Login/Register forms
   - Vehicle listings with search/filter
   - Vehicle detail pages
   - Booking forms
   - User profile management
   - Booking history

2. **Add advanced features**:
   - Real-time availability updates
   - Payment gateway integration
   - Email notifications
   - SMS alerts
   - Driver assignment system

3. **Enhancements**:
   - Image upload functionality
   - Advanced search and filtering
   - Booking calendar view
   - Admin dashboard improvements
   - Mobile app development

## 📞 Contact Information

- **Phone**: +92-300-0000000
- **Facebook**: facebook.com/AwanRentACar
- **Instagram**: instagram.com/AwanRentACar
- **WhatsApp**: +92-300-0000000
- **Email**: info@awanrentacar.com

## 📄 License

This project is for demonstration purposes and educational use.
