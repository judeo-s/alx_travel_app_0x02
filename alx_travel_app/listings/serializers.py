from rest_framework import serializers
from .models import Listing, Booking, Payment

class ListingSerializer(serializers.ModelSerializer):
    """Serializer for the Listing model"""
    
    class Meta:
        model = Listing
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for the Booking model"""
    
    class Meta:
        model = Booking
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model"""
    class Meta:
        model = Payment
        fields = '__all__'
