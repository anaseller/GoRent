from rest_framework import permissions


class IsLandlord(permissions.BasePermission):
    """
    The user has the right only if they are the landlord.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_landlord

    def has_object_permission(self, request, view, obj):
        # Allows access only if the object belongs to the landlord
        # use obj.listing.landlord for bookings
        # and obj.landlord for listings
        if hasattr(obj, 'landlord'):
            return obj.landlord == request.user
        elif hasattr(obj, 'listing'):
            return obj.listing.landlord == request.user
        return False
