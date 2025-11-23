import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from django.db import IntegrityError
from datetime import date, timedelta

# --- Configuration ---
NUM_USERS = 5
NUM_LISTINGS = 10
BOOKINGS_PER_LISTING = 3
REVIEWS_PER_LISTING = 4

# --- Sample Data ---
COUNTRIES = ['USA', 'Canada', 'UK', 'Australia', 'Germany', 'France']
CITIES = ['New York', 'Toronto', 'London', 'Sydney', 'Berlin', 'Paris']
LISTING_TITLES = [
    "Cozy Downtown Loft", "Sunny Beachfront Villa", "Rustic Mountain Cabin",
    "Modern City Apartment", "Charming Cottage by the Lake", "Executive Studio"
]

class Command(BaseCommand):
    help = 'Seeds the database with sample users, listings, bookings, and reviews.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting database seeding...'))

        # 1. Clear existing sample data
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        # Delete only the seeded users to protect the admin user
        User.objects.filter(username__startswith='seed_user_').delete()
        
        self.stdout.write(self.style.WARNING('Existing sample data cleared.'))

        # 2. Create Sample Users
        self.stdout.write(self.style.NOTICE(f'Creating {NUM_USERS} sample users...'))
        users = []
        for i in range(1, NUM_USERS + 1):
            username = f'seed_user_{i}'
            email = f'user{i}@example.com'
            user, created = User.objects.get_or_create(
                username=username, 
                defaults={'email': email, 'is_staff': False}
            )
            if created:
                user.set_password('password') 
                user.save()
            users.append(user)
        self.stdout.write(self.style.SUCCESS('Users created successfully.'))


        # 3. Create Sample Listings
        self.stdout.write(self.style.NOTICE(f'Creating {NUM_LISTINGS} sample listings...'))
        listings = []
        for i in range(1, NUM_LISTINGS + 1):
            host = random.choice(users)
            title = random.choice(LISTING_TITLES) + f" #{i}"
            country = random.choice(COUNTRIES)
            city = random.choice(CITIES)
            
            listing = Listing(
                host=host,
                title=title,
                description=f"Description for {title}. A beautiful place in {city}, {country}.",
                price_per_night=round(random.uniform(50, 300), 2),
                country=country,
                city=city,
                address=f"{random.randint(100, 999)} Sample St.",
                is_published=True
            )
            listing.save()
            listings.append(listing)
        self.stdout.write(self.style.SUCCESS('Listings created successfully.'))


        # 4. Create Sample Bookings
        self.stdout.write(self.style.NOTICE('Creating sample bookings...'))
        today = date.today()
        for listing in listings:
            for _ in range(BOOKINGS_PER_LISTING):
                guest = random.choice(users)
                if guest == listing.host: 
                    continue

                start_offset = random.randint(1, 30)
                duration = random.randint(2, 7)
                start_date = today + timedelta(days=start_offset)
                end_date = start_date + timedelta(days=duration)
                total_price = listing.price_per_night * duration
                
                try:
                    Booking.objects.create(
                        listing=listing,
                        guest=guest,
                        start_date=start_date,
                        end_date=end_date,
                        total_price=total_price,
                        is_paid=random.choice([True, False])
                    )
                except IntegrityError:
                    pass 
        self.stdout.write(self.style.SUCCESS('Bookings created successfully.'))


        # 5. Create Sample Reviews
        self.stdout.write(self.style.NOTICE('Creating sample reviews...'))
        for listing in listings:
            # Get users who are not the host and have not already reviewed this listing
            potential_reviewers = [
                u for u in users 
                if u != listing.host and not Review.objects.filter(listing=listing, reviewer=u).exists()
            ]
            
            reviewers = random.sample(potential_reviewers, min(len(potential_reviewers), REVIEWS_PER_LISTING))
            
            for reviewer in reviewers:
                rating = random.randint(1, 5)
                comment = random.choice([
                    "Fantastic stay! Highly recommend.", 
                    "Clean and comfortable.", 
                    "Great value for money.", 
                    None 
                ])
                
                try:
                    Review.objects.create(
                        listing=listing,
                        reviewer=reviewer,
                        rating=rating,
                        comment=comment
                    )
                except IntegrityError:
                    pass 
        self.stdout.write(self.style.SUCCESS('Reviews created successfully.'))

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))

