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


class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class KitchenList(generics.ListCreateAPIView):
    queryset = Kitchen.objects.all()
    serializer_class = serializers.KitchenSerializer


class KitchenDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kitchen.objects.all()
    serializer_class = serializers.KitchenSerializer


class FoodList(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = serializers.FoodSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FoodDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = serializers.FoodSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


'''Главная страница'''


class RestaurantList(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantRetrieveSerializer


class RestaurantCreate(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
