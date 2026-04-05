from rest_framework import serializers
from .models import Ad, Review, Category, City

class ReviewSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Review
        fields = ['id', 'author_username', 'text', 'rating', 'created_at']

class AdSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    city_name = serializers.ReadOnlyField(source='city.name')
    
    # Достаем все отзывы, связанные с этим объявлением (related_name='reviews' в модели)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = [
            'uuid', 
            'title', 
            'description', 
            'price', 
            'image', 
            'author_username', 
            'category_name', 
            'city_name', 
            'created_at',
            'reviews'  # Теперь отзывы полетят во Флаттер вместе с объявой
        ]