from rest_framework import serializers
from stores.models import *


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'restaurants']


class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = ['id', 'title']


class RestaurantCreateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'time', 'image', 'owner', 'kitchen']


class RestaurantRetrieveSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    kitchen = KitchenSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'slug', 'time', 'image', 'owner', 'kitchen']
        lookup_field = 'slug'


class FoodRetrieveSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Food
        fields = ['id', 'title', 'description', 'image', 'price', 'owner']


class FoodCreateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Food
        fields = ['id', 'title', 'description', 'image', 'price', 'owner', 'categories', 'restaurants']
