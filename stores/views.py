from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_list_or_404
from rest_framework import status, viewsets
from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
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

    def update(self, request, *args, **kwargs):
        if 'kitchen[]' in request.data:
            request.data._mutable = True
            request.data.setlist('kitchen', request.data.pop('kitchen[]'))
        return super().update(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['restaurants']


class KitchenViewSet(viewsets.ModelViewSet):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer


class FoodListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'food': data
        })


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodRetrieveSerializer
    pagination_class = FoodListPagination
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
