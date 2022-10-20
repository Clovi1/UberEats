from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_list_or_404
from rest_framework import status, viewsets
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from .models import *


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RestaurantRetrieveSerializer
        else:
            return RestaurantCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['restaurants']


class KitchenViewSet(viewsets.ModelViewSet):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodRetrieveSerializer
    filterset_fields = ['restaurants', 'categories']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return FoodRetrieveSerializer
        else:
            return FoodCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        categories = instance.categories.all()
        for category in categories:
            if category.food.filter(restaurants=instance.restaurants).count() <= 1:
                instance.restaurants.categories.remove(category)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
