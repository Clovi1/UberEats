from rest_framework import serializers
from django.contrib.auth.models import User

from stores.models import *


class UserSerializer(serializers.ModelSerializer):
    restaurants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'restaurants']


class RestaurantSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # food = serializers.StringRelatedField(many=True, source='food__title')
    # food = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'slug', 'time', 'image', 'owner', 'kitchen', 'food', 'categories']


class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = ['id', 'title']


class CategoriesTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']


class FoodSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Food
        fields = ['id', 'title', 'description', 'image', 'price', 'owner', 'restaurants', 'categories']

    def create(self, validated_data):
        categories = validated_data.pop('categories')
        food = Food.objects.create(**validated_data)
        food.categories.set(categories)
        for category in categories:
            food.restaurants.categories.add(category.pk)
        return food

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories')
        instance.categories.set(categories)
        # instance.restaurants.categories.set(categories)
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


'''Главная страница'''


class KitchenInRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = ['id', 'title']


class RestaurantRetrieveSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    kitchen = KitchenInRestaurantSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'slug', 'time', 'image', 'owner', 'kitchen']
        # depth = 1


class RestaurantCreateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'time', 'image', 'owner', 'kitchen']
