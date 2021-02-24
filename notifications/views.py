from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import permissions, generics, status

from rest_framework_serializer_extensions.utils import (
    internal_id_from_model_and_external_id,
)

from hunchat.model_loaders import get_notification_model
from hunchat import permissions as friendzone_permissions

from notifications.serializers import NotificationSerializer


class Notifications(generics.ListAPIView):
    """
    API endpoint to list user notifications.
    """

    serializer_class = NotificationSerializer
    permission_classes = [friendzone_permissions.IsAdminOrIsOwner]

    def get_queryset(self, pk):
        """Get user's chat rooms."""
        user = get_user_model().objects.get(pk=pk)
        notifications = user.notifications.all()
        return notifications

    def get(self, request, pk):
        """Returns user's chat rooms"""
        pk = internal_id_from_model_and_external_id(User, pk)
        notifications = self.get_queryset(pk=pk)
        serializer = self.serializer_class(notifications, many=True)
        return Response(data={"results": serializer.data}, status=status.HTTP_200_OK)
