from django.shortcuts import render
from rest_framework import viewsets, status
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer
import uuid
from .celery import send_payment_confirmation_email

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class InitiatePaymentView(APIView):
    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id)
            tx_ref = str(uuid.uuid4())
            amount = float(booking.listing_id.price_per_night)

            headers = {
                'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
                'Content-Type': 'application/json',
            }

            payload = {
                'amount': amount,
                'currency': 'ETB',
                'email': 'okeleji.azeez@gmail.com', # booking.user_id.email,
                'tx_ref': tx_ref,
                'callback_url': f'http://localhost:8000/api/payments/verify/{tx_ref}/',
                'return_url': 'http://localhost:8000/payment-success/',
                'customization[title]': 'ALX Travel Booking Payment',
            }

            response = requests.post('https://api.chapa.co/v1/transaction/initialize', headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()['data']
                payment = Payment.objects.create(
                    booking=booking,
                    amount=amount,
                    chapa_tx_ref=tx_ref,
                    chapa_checkout_url=data['checkout_url'],
                    status='Pending'
                )
                return Response({'checkout_url': data['checkout_url']}, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Payment Initiation Failed',
                    'details': response.json()
                 }, status=response.status_code)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

class VerifyPaymentView(APIView):
    def get(self, request, tx_ref):
        try:
            payment = Payment.objects.get(chapa_tx_ref=tx_ref)

            response = requests.get(
                f"https://api.chapa.co/v1/transaction/verify/{tx_ref}",
                headers={'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'}
            )

            if response.status_code == 200:
                result = response.json()['data']
                if result['status'] == 'success':
                    payment.status = 'Completed'
                    payment.save()
                    # celery email
                    send_payment_confirmation_email(
                        payment.booking.user_id.email,
                        payment.booking.booking_id
                    )
                    return Response({'message': 'Payment Verified and Completed'})
                else:
                    payment.status = 'Failed'
                    payment.save()
                    return Response({'message': 'Payment Failed'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Verification Failed'}, status=response.status_code)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
