from rest_framework import permissions


class IsAdminOrIsSelf(permissions.IsAuthenticated):
    """
    Give permission to admin users or the user himself.
    """

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        elif request.user and type(obj) == type(request.user) and obj == request.user:
            return True
        return False


class IsAdminOrIsOwner(permissions.IsAuthenticated):
    """
    Give permission to admin users or the owner of the instance.
    """

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        elif (
            request.user
            and type(obj.user) == type(request.user)
            and obj.user == request.user
        ):
            return True
        return False
