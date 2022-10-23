from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from stores import views

router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurants')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'kitchen', views.KitchenViewSet, basename='kitchen')
router.register(r'food', views.FoodViewSet, basename='food')
router.register(r'users', views.UserRetrieveViewSet, basename='users')

urlpatterns = [
    # Главная страница
    path('', include(router.urls)),

    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    # path('auth/', include('djoser.urls.jwt')),
    #
    # path('api/token/', TokenObtainPairView.as_view()),
    # path('api/token/refresh/', TokenRefreshView.as_view()),
    # path('api/token/verify/', TokenVerifyView.as_view()),
]
