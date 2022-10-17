from django.urls import path

from stores import views

urlpatterns = [
    # Главная страница
    path('restaurants/', views.RestaurantList.as_view(), name='restaurants'),
    path('restaurants/<slug:slug>/', views.RestaurantDetail.as_view(), name='restaurant_detail'),

    path('restaurants/update/<slug:slug>/', views.RestaurantUpdate.as_view(), name='update_restaurant'),
    # path('restaurants/<int:pk>/', views.RestaurantDetail.as_view(), name='restaurant_pk'),
    path('restaurants/category/', views.FoodList.as_view(), name='food'),

    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

    path('kitchen/', views.KitchenList.as_view()),
    # path('kitchen/<int:pk>/', views.KitchenDetail.as_view()),

    path('foodold/', views.FoodOldList.as_view()),
    # path('foodold/<int:pk>/', views.FoodDetail.as_view()),

    path('category/', views.CategoryList.as_view()),
    # path('category/<int:pk>/', views.CategoryDetail.as_view()),
]
