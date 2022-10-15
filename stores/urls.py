from django.urls import path

from stores import views

urlpatterns = [
    # Главная страница
    path('restaurants/', views.RestaurantList.as_view(), name='restaurants'),
    path('restaurants/create/', views.RestaurantCreate.as_view(), name='create_restaurants'),
    # path('restaurants/<int:pk>/', views.RestaurantDetail.as_view(), name='restaurant_pk'),
    path('restaurants/<slug:slug>/', views.RestaurantDetail.as_view(), name='restaurant_slug'),

    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

    path('kitchen/', views.KitchenList.as_view()),
    path('kitchen/<int:pk>/', views.KitchenDetail.as_view()),

    path('food/', views.FoodList.as_view()),
    path('food/<int:pk>/', views.FoodDetail.as_view()),

    path('category/', views.CategoryList.as_view()),
    path('category/<int:pk>/', views.CategoryDetail.as_view()),
]
