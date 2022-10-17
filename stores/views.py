from django.core.exceptions import ObjectDoesNotExist
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
# # class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
# #     queryset = Restaurant.objects.all()
# #     serializer_class = serializers.RestaurantSerializer
#
#
class KitchenList(ListCreateAPIView):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenSerializer


#
# class KitchenDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Kitchen.objects.all()
#     serializer_class = KitchenSerializer
#
#
class FoodOldList(ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


#
# class FoodDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Food.objects.all()
#     serializer_class = FoodCreateSerializer
#

class CategoryList(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


#
# class CategoryDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#

'''Главная страница'''


class RestaurantList(APIView):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        data = RestaurantListSerializer(restaurants, many=True).data
        return Response({'restaurants': data})

    def post(self, request):
        serializer = RestaurantCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response({'Success': 'Ресторан удачно создан', 'Рестораны': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response({'Fail': 'Ошибка в создании ресторана', 'Errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class RestaurantDetail(APIView):
    """"""
    lookup_field = 'slug'

    def get_object(self, slug):
        try:
            return Restaurant.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({'Fail': 'Такого ресторана не существует'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, slug):
        # Получение ресторана
        restaurant = self.get_object(slug)
        if isinstance(restaurant, Response): return restaurant
        restaurant_serializer = RestaurantDetailSerializer(restaurant)

        # Получение еды
        pk = request.query_params.get('category')
        food = Food.objects.filter(categories=pk, restaurants=restaurant.pk)
        food_serializer = FoodSerializer(food, many=True)

        return Response({'restaurant': restaurant_serializer.data, 'food': food_serializer.data},
                        status=status.HTTP_200_OK)

    def delete(self, request, pk):
        restaurant = self.get_restaurant(pk)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RestaurantUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantUpdateSerializer
    lookup_field = 'slug'


class FoodList(ListAPIView):
    serializer_class = FoodSerializer

    def get_queryset(self):
        queryset = Food.objects.all()
        restaurant = self.request.query_params.get('restaurant')
        category = self.request.query_params.get('category')
        if restaurant and category:
            queryset = queryset.filter(restaurants=restaurant, categories=category)

        return queryset
