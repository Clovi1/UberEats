from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_list_or_404
from rest_framework import status, viewsets
from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

from rest_framework.views import APIView

from pagination import FoodListPagination
from .permissions import IsOwnerOrAdminOrReadOnly, IsRestaurantOwnerOrReadOnly, IsRestaurantOwnerObjectOrReadOnly
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend

from .models import *


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RestaurantRetrieveSerializer
        else:
            return RestaurantCreateSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsOwnerOrAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        if 'kitchen' not in request.data and request.data:
            request.data._mutable = True
            lst = []
            if 'kitchen[]' in request.data:
                lst = [*request.data.pop('kitchen[]')]

            if 'new_kitchen[]' in request.data:
                new_kitchen = list(map(lambda x: x.lower(), request.data.pop('new_kitchen[]')))
                for title in new_kitchen:
                    if title:
                        kitchen = Kitchen.objects.filter(title=title).first()
                        if kitchen:
                            lst.append(kitchen.pk)
                        else:
                            lst.append(Kitchen.objects.create(title=title).pk)
            if lst:
                request.data.setlist('kitchen', lst)
            request.data._mutable = False
        return super().update(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    filterset_fields = ['restaurants']
    permission_classes = [IsRestaurantOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return CategoryRetrieveSerializer
        else:
            return CategoryCreateSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsRestaurantOwnerOrReadOnly]
        else:
            permission_classes = [IsRestaurantOwnerObjectOrReadOnly]
        return [permission() for permission in permission_classes]


class KitchenViewSet(viewsets.ModelViewSet):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodRetrieveSerializer
    pagination_class = FoodListPagination
    filterset_fields = ['restaurants','categories']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return FoodRetrieveSerializer
        else:
            return FoodCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsRestaurantOwnerOrReadOnly]
        else:
            permission_classes = [IsRestaurantOwnerObjectOrReadOnly]
        return [permission() for permission in permission_classes]
