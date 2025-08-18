from rest_framework import permissions


class IsLandlord(permissions.BasePermission):
    """
    The user has the right only if they are the landlord.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_landlord

    def has_object_permission(self, request, view, obj):
        # GET-запросы доступны любому, но только арендодатель может редактировать и удалять
        if request.method in permissions.SAFE_METHODS:
            return True

        # Только владелец объявления может его редактировать или удалять
        return obj.landlord == request.user