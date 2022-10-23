from django.db.models import Count
from rest_framework import serializers
from django.contrib.auth.models import User

from stores.models import *


class UserRetrieveSerializer(serializers.ModelSerializer):
    restaurants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'restaurants']


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    restaurants = serializers.StringRelatedField(read_only=True, source='restaurants.title')

    class Meta:
        model = Category
        fields = ['id', 'title', 'restaurants']


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

    # def create(self, validated_data):
    #     categories = validated_data.pop('categories')
    #     food = Food.objects.create(**validated_data)
    #     food.categories.set(categories)
    #     for category in categories:
    #         food.restaurants.categories.add(category.pk)
    #     return food
    #
    # def update(self, instance, validated_data):
    #     categories = instance.categories.all()
    #     for category in categories:
    #         if category.food.filter(restaurants=instance.restaurants).count() <= 1:
    #             instance.restaurants.categories.remove(category)
    #
    #     categories = validated_data.pop('categories')
    #     instance.categories.set(categories)
    #     for category in categories:
    #         instance.restaurants.categories.add(category.pk)
    #     return super().update(instance, validated_data)
