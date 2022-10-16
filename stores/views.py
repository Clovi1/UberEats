from rest_framework import generics
from . import serializers
from django.contrib.auth.models import User

from .models import *


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


# class RestaurantList(generics.ListCreateAPIView):
#     queryset = Restaurant.objects.all()
#     serializer_class = serializers.RestaurantSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Restaurant.objects.all()
#     serializer_class = serializers.RestaurantSerializer


class KitchenList(generics.ListCreateAPIView):
    queryset = Kitchen.objects.all()
    serializer_class = serializers.KitchenSerializer


class KitchenDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kitchen.objects.all()
    serializer_class = serializers.KitchenSerializer


class FoodOldList(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = serializers.FoodCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FoodDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = serializers.FoodCreateSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


'''Главная страница'''


class RestaurantList(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantListSerializer


class RestaurantCreate(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RestaurantDetail(generics.RetrieveDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantDetailSerializer
    lookup_field = 'slug'

    # def get_queryset(self):
    #     queryset = Restaurant.objects.all()
    #     category = self.request.query_params.get('category')
    #     if category:
    #         queryset = queryset.filter(food__categories=category)
    #     return queryset


class RestaurantUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantUpdateSerializer
    lookup_field = 'slug'


class FoodList(generics.ListAPIView):
    serializer_class = serializers.FoodSerializer

    def get_queryset(self):
        queryset = Food.objects.all()
        restaurant = self.request.query_params.get('restaurant')
        category = self.request.query_params.get('category')
        if restaurant and category:
            queryset = queryset.filter(restaurants=restaurant, categories=category)

        return queryset
