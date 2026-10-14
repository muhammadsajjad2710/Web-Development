from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Booking, BookingPayment
from .serializers import (
    BookingSerializer, BookingCreateSerializer, 
    BookingListSerializer, BookingPaymentSerializer
)
from vehicles.models import Vehicle


class BookingListView(generics.ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Calculate total amount
        vehicle = Vehicle.objects.get(id=serializer.validated_data['vehicle_id'])
        booking_type = serializer.validated_data['booking_type']
        
        if booking_type == 'local':
            pickup_date = datetime.fromisoformat(serializer.validated_data['pickup_date'].replace('Z', '+00:00'))
            return_date = datetime.fromisoformat(serializer.validated_data['return_date'].replace('Z', '+00:00'))
            days = (return_date - pickup_date).days + 1
            total_amount = vehicle.daily_rate * days
        else:
            # Intercity trip - use daily rate for now
            total_amount = vehicle.daily_rate
        
        # Create booking
        booking_data = serializer.validated_data.copy()
        booking_data['user'] = request.user
        booking_data['total_amount'] = total_amount
        
        booking = Booking.objects.create(**booking_data)
        
        # Create payment record
        BookingPayment.objects.create(
            booking=booking,
            amount=total_amount,
            payment_method='cash',  # Default to cash
            payment_status='pending'
        )
        
        response_serializer = BookingSerializer(booking)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class BookingUpdateView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingCancelView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.status in ['confirmed', 'pending']:
            booking.status = 'cancelled'
            booking.save()
            return Response({'message': 'Booking cancelled successfully'})
        return Response({'error': 'Cannot cancel this booking'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_bookings(request):
    """Get all bookings for the current user"""
    bookings = Booking.objects.filter(user=request.user)
    serializer = BookingListSerializer(bookings, many=True)
    return Response(serializer.data)
