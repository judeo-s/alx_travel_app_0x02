# alx_travel_app_0x02

## Setup

1. Clone the repository.
2. Install dependencies.
3. Configure `.env` for MySQL and other settings.
4. Run migrations:
python manage.py makemigrations
python manage.py migrate
5. Seed the database:
python manage.py seed

## Swagger

API Documentation is available at: `http://localhost:8000/swagger/`

## Core Models

- **Listing**: Properties listed by hosts.
- **Booking**: Reservations made by guests.
- **Review**: Ratings/comments left by users.
- **Payment**: Payments by users.
