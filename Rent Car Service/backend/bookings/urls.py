from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('bookings/', views.BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking-update'),
    path('bookings/<int:pk>/cancel/', views.BookingCancelView.as_view(), name='booking-cancel'),
    path('bookings/user/', views.user_bookings, name='user-bookings'),
]
