from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_payment_confirmation_email(user_email, booking_id):
    send_mail(
        subject='Payment Confirmation',
        message=f'Your payment for Booking {booking_id} has been confirmed.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )
