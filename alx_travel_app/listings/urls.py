from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ListingViewSet, BookingViewSet, InitiatePaymentView, VerifyPaymentView

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = router.urls + [
    path('payments/initiate/<int:booking_id>/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payments/verify/<str:tx_ref>/', VerifyPaymentView.as_view(), name='verify-payment'),
]
