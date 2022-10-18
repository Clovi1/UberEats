from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_list_or_404
from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from django.contrib.auth.models import User

from .models import *


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# # class RestaurantList(generics.ListCreateAPIView):
# #     queryset = Restaurant.objects.all()
# #     serializer_class = serializers.RestaurantSerializer
# #
# #     def perform_create(self, serializer):
# #         serializer.save(owner=self.request.user)
#
#
# # class RestaurantRetrieve(generics.RetrieveUpdateDestroyAPIView):
# #     queryset = Restaurant.objects.all()
# #     serializer_class = serializers.RestaurantSerializer
#
#
# class FoodOldList(ListCreateAPIView):
#     queryset = Food.objects.all()
#     serializer_class = FoodCreateSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


#

'''Главная страница'''


class RestaurantList(APIView):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        data = RestaurantListSerializer(restaurants, many=True, context={"request": request}).data
        return Response({'restaurants': data})

    def post(self, request):
        serializer = RestaurantCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response({'Success': 'Ресторан удачно создан', 'Рестораны': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response({'Fail': 'Ошибка в создании ресторана', 'Errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class RestaurantRetrieve(ListCreateAPIView):
    """Страница ресторана"""

    # lookup_field = 'slug'
    #
    # def get_object(self, slug):
    #     try:
    #         return Restaurant.objects.get(slug=slug)
    #     except ObjectDoesNotExist:
    #         return Response({'Fail': 'Такого ресторана не существует'}, status=status.HTTP_404_NOT_FOUND)
    #
    # def get(self, request, slug):
    #     # Получение ресторана
    #     restaurant = self.get_object(slug)
    #     if isinstance(restaurant, Response): return restaurant
    #     restaurant_serializer = RestaurantDetailSerializer(restaurant, context={"request": request})
    #
    #     # Получение еды
    #     pk = request.query_params.get('category')
    #     food = Food.objects.filter(categories=pk, restaurants=restaurant.pk)
    #     food_serializer = FoodListSerializer(food, many=True, context={"request": request})
    #
    #     return Response({'restaurant': restaurant_serializer.data, 'food': food_serializer.data},
    #                     status=status.HTTP_200_OK)


class RestaurantDetail(RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantCreateSerializer
    lookup_field = 'slug'

    # def get_object(self, slug):
    #     try:
    #         return Restaurant.objects.get(slug=slug)
    #     except ObjectDoesNotExist:
    #         return Response({'Fail': 'Такого ресторана не существует'}, status=status.HTTP_404_NOT_FOUND)
    #
    # def get(self, request, slug):
    #     restaurant = self.get_object(slug)
    #     if isinstance(restaurant, Response): return restaurant
    #     serializer = RestaurantDetailSerializer(restaurant, context={"request": request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def put(self, request, slug):
    #     restaurant = self.get_object(slug)
    #     if isinstance(restaurant, Response): return restaurant
    #     serializer = RestaurantCreateSerializer(restaurant, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class KitchenList(ListCreateAPIView):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer


class KitchenDetail(RetrieveUpdateDestroyAPIView):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer


class CategoryList(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
