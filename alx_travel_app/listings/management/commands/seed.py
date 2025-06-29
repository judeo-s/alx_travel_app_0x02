#!/usr/bin/env python3

from django.core.management.base import BaseCommand
from listings.models import Listing, Booking, Review
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

class Command(BaseCommand):
    help = 'Seed the database with sample Listings, Bookings, and Reviews.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Create users
        user1, _ = User.objects.get_or_create(username='host1', defaults={'email': 'host1@example.com'})
        user2, _ = User.objects.get_or_create(username='host2', defaults={'email': 'host2@example.com'})
        user3, _ = User.objects.get_or_create(username='guest1', defaults={'email': 'guest1@example.com'})

        # Create listings
        listing1 = Listing.objects.create(
            listing_id=1,
            title="Quillox",
            description="Luxury Nightlife with lounge and club",
            location="Victoria Island, Lagos",
            price_per_night=16000,
            available_from=datetime(2025, 9, 10),
            available_to=datetime(2025, 10, 9),
            host_id=user1
        )

        listing2 = Listing.objects.create(
            listing_id=2,
            title="Lagos Country Club",
            description="This is a luxurious property, best for your relaxation",
            location="Isaac John street, Ikeja, Lagos",
            price_per_night=20000,
            available_from=datetime(2025, 9, 10),
            available_to=datetime(2026, 10, 9),
            host_id=user2
        )

        listing3 = Listing.objects.create(
            listing_id=3,
            title="Palm Avenue Estate",
            description="A perfect place to enjoy light 24/7",
            location="124, Isolo Road, Mushin",
            price_per_night=500000,
            available_from=datetime(2024, 9, 10),
            available_to=datetime(2025, 10, 9),
            host_id=user1
        )

        # Create bookings
        Booking.objects.create(
            booking_id=1,
            listing_id=listing1,
            user_id=user3,
            start_date="2024-12-01",
            end_date="2024-12-05",
            total_price=2000000,
            status="confirmed"
        )

        Booking.objects.create(
            booking_id=2,
            listing_id=listing2,
            user_id=user3,
            start_date="2024-11-20",
            end_date="2024-11-22",
            total_price=2000000,
            status="pending"
        )

        Booking.objects.create(
            booking_id=3,
            listing_id=listing3,
            user_id=user2,
            start_date="2024-10-10",
            end_date="2024-10-15",
            total_price=2000000,
            status="canceled"
        )

        # Create reviews
        Review.objects.create(
            review_id=1,
            listing_id=listing1,
            user_id=user3,
            rating=5,
            comment="Amazing stay. Will book again!",
            created_at=datetime(2025, 10, 20)
        )

        Review.objects.create(
            review_id=2,
            listing_id=listing2,
            user_id=user1,
            rating=3,
            comment="Decent, but could be cleaner.",
            created_at=datetime(2024, 12, 10)
        )

        Review.objects.create(
            review_id=3,
            listing_id=listing3,
            user_id=user2,
            rating=4,
            comment="Comfortable and quiet. Great service.",
            created_at=datetime(2024, 12, 25)
        )

        self.stdout.write(self.style.SUCCESS('✅ Successfully seeded the database with sample data.'))
