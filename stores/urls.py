from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stores import views

router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurants')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'kitchen', views.KitchenViewSet, basename='kitchen')

urlpatterns = [
    # Главная страница
    path('', include(router.urls)),

    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

    path('food/', views.FoodList.as_view()),
    path('food/<int:pk>/', views.FoodDetail.as_view()),

    # path('foodold/', views.FoodOldList.as_view()),

]
