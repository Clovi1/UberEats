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


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RestaurantRetrieveSerializer
        else:
            return RestaurantSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['restaurants']


class KitchenViewSet(viewsets.ModelViewSet):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer


# ----------------------------------------------------------
class FoodList(ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# def get(self, request):
#     food = Food.objects.all()
#     data = FoodListSerializer(food, many=True, context={"request": request}).data
#     return Response({'food': data})
#
# def post(self, request):
#     serializer = FoodCreateSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(owner=self.request.user)
#         return Response({'Success': 'Блюдо удачно создано', 'food': serializer.data},
#                         status=status.HTTP_201_CREATED)
#     return Response({'Fail': 'Ошибка в создании блюда', 'Errors': serializer.errors},
#                     status=status.HTTP_400_BAD_REQUEST)

class FoodDetail(RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodListSerializer
