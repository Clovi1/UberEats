from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from stores import views

router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurants')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'kitchen', views.KitchenViewSet, basename='kitchen')
router.register(r'food', views.FoodViewSet, basename='food')

urlpatterns = [
    # Главная страница
    path('', include(router.urls)),

    path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),

    path('user/', include('rest_framework.urls'))
]
