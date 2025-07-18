from django.db import models

class Listing(models.Model):
    """Model for property listings"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    """Model for bookings"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    user_name = models.CharField(max_length=255)  # Assuming a simple name field instead of FK to User model
    user_email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.user_name}"


class Review(models.Model):
    class Rating(models.IntegerChoices):
        ONE = 1, '1 - Poor'
        TWO = 2, '2 - Fair'
        THREE = 3, '3 - Good'
        FOUR = 4, '4 - Very Good'
        FIVE = 5, '5 - Excellent'
    review_id = models.IntegerField(primary_key=True)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=Rating.choices, default=Rating.THREE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user_id.username} for {self.listing_id.title}"


class Payment(models.Model):
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed")
    ], default="Pending")
    chapa_tx_ref = models.CharField(max_length=100, unique=True)
    chapa_checkout_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.booking_id}"
