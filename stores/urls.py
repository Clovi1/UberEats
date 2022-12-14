from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stores import views

router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurants')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'kitchen', views.KitchenViewSet, basename='kitchen')
router.register(r'food', views.FoodViewSet, basename='food')

urlpatterns = [
    path('', include(router.urls)),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # path('auth/', include('djoser.urls.authtoken')),

    path('user/', include('rest_framework.urls'))
]
