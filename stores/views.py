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


class UserRetrieveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer


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
        request.data._mutable = True
        if 'kitchen[]' in request.data:
            request.data.setlist('kitchen', request.data.pop('kitchen[]'))

        if 'new_kitchen[]' in request.data:
            new_kitchen = request.data.pop('new_kitchen[]')
            instance = self.get_object()
            for title in new_kitchen:
                if title:
                    kitchen = Kitchen.objects.filter(title=title).first()
                    if kitchen:
                        instance.kitchen.add(kitchen)
                    else:
                        instance.kitchen.add(Kitchen.objects.create(title=title))
        request.data._mutable = False
        return super().update(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    filterset_fields = ['restaurants']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return CategoryRetrieveSerializer
        else:
            return CategoryCreateSerializer


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
    filterset_fields = ['categories']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return FoodRetrieveSerializer
        else:
            return FoodCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
