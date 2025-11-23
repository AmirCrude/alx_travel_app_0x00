from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import F, Q

# --- Listing Model ---
class Listing(models.Model):
    # Core Fields
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)] 
    )
    is_published = models.BooleanField(default=False)
    
    # Location/Details
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationship: Host/Owner (One-to-Many with User)
    host = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='listings' # Allows user_instance.listings.all()
    )

    def __str__(self):
        return self.title

# --- Booking Model ---
class Booking(models.Model):
    # Relationship: Listing (Many-to-One)
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    
    # Relationship: Guest (Many-to-One with User)
    guest = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )

    # Core Fields
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking for {self.listing.title} by {self.guest.username}"
    
    class Meta:
        constraints = [
            # Ensures logical date order at the database level
            models.CheckConstraint(
                check=Q(start_date__lt=F('end_date')),
                name='start_date_before_end_date'
            )
        ]

# --- Review Model ---
class Review(models.Model):
    # Relationship: Listing (Many-to-One)
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    
    # Relationship: Reviewer (Many-to-One with User)
    reviewer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )

    # Core Fields
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)] # Rating from 1 to 5
    )
    comment = models.TextField(blank=True, null=True)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.listing.title} ({self.rating}/5)"
    
    class Meta:
        # Ensures uniqueness: One reviewer, one review per listing
        unique_together = ('listing', 'reviewer')