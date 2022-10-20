from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stores import views

router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurants')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'kitchen', views.KitchenViewSet, basename='kitchen')
router.register(r'food', views.FoodViewSet, basename='food')
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    # Главная страница
    path('', include(router.urls)),
]
