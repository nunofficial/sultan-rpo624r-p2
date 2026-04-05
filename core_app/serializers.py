from rest_framework import serializers
from .models import Ad

class AdSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    city_name = serializers.ReadOnlyField(source='city.name')

    class Meta:
        model = Ad
        fields = ['uuid', 'title', 'description', 'price', 'image', 'author_username', 'category_name', 'city_name', 'created_at']