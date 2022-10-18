from rest_framework import serializers
from django.contrib.auth.models import User

from stores.models import *


class UserSerializer(serializers.ModelSerializer):
    restaurants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'restaurants']


# class FoodCreateSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#
#     class Meta:
#         model = Food
#         fields = ['id', 'title', 'description', 'image', 'price', 'owner', 'restaurants', 'categories']
#
#     def create(self, validated_data):
#         categories = validated_data.pop('categories')
#         food = Food.objects.create(**validated_data)
#         food.categories.set(categories)
#         for category in categories:
#             food.restaurants.categories.add(category.pk)
#         return food

# def update(self, instance, validated_data):
#     categories = validated_data.pop('categories')
#     instance.categories.set(categories)
#     # instance.restaurants.categories.set(categories)
#     instance.save()
#     return instance


'''Главная страница'''


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = ['id', 'title']


class RestaurantListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    kitchen = KitchenSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'slug', 'time', 'image', 'owner', 'kitchen']


class RestaurantCreateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    kitchen = KitchenSerializer(many=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'time', 'image', 'owner', 'kitchen']


class FoodListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    categories = CategorySerializer(many=True)

    class Meta:
        model = Food
        fields = ['id', 'title', 'description', 'image', 'price', 'owner', 'categories']


class FoodCreateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Food
        fields = ['id', 'title', 'description', 'image', 'price', 'owner', 'categories']


class RestaurantDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    kitchen = KitchenSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'slug', 'time', 'image', 'owner', 'kitchen']
        lookup_fields = 'slug'


class RestaurantUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'slug', 'time', 'image', 'owner', 'kitchen', 'food', 'categories']
        lookup_field = 'slug'
