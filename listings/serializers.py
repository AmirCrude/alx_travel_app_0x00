from rest_framework import serializers
from .models import Listing, Booking, Review

# --- Review Serializer (for nesting) ---
class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'reviewer_username', 'rating', 'comment', 'created_at']

# --- Booking Serializer ---
class BookingSerializer(serializers.ModelSerializer):
    guest_username = serializers.CharField(source='guest.username', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'guest', 'guest_username', 
            'start_date', 'end_date', 'total_price', 'is_paid', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

# --- Listing Serializer ---
class ListingSerializer(serializers.ModelSerializer):
    host_username = serializers.CharField(source='host.username', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True) 
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price_per_night', 'country', 'city', 
            'address', 'is_published', 'host', 'host_username', 'reviews', 
            'average_rating', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'host'] 
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0.0
        total_rating = sum([review.rating for review in reviews])
        return round(total_rating / len(reviews), 2)