from rest_framework import permissions

from stores.models import Restaurant, Category


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_staff or
            obj.owner == request.user
        )


class IsRestaurantOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'restaurants' in request.query_params:
            restaurant = Restaurant.objects.get(pk=request.query_params.get('restaurants')).owner == request.user
        else:
            restaurant = False

        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_staff or
            restaurant
        )


class IsRestaurantOwnerObjectOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_staff or
            obj.restaurants.owner == request.user
        )
