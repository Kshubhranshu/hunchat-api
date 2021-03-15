from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from rest_framework_serializer_extensions.utils import (
    internal_id_from_model_and_external_id,
)

from hunchat import permissions as hunchat_permissions

from notifications.serializers import NotificationSerializer


class Notifications(APIView):
    """
    API endpoint to list user notifications.
    """

    serializer_class = NotificationSerializer
    permission_classes = [hunchat_permissions.IsAdminOrIsOwner]

    def get(self, request, pk):
        """Returns user's notifications"""
        pk = internal_id_from_model_and_external_id(get_user_model(), pk)
        user = get_user_model().objects.get(pk=pk)
        notifications = user.notifications.all()
        serializer = self.serializer_class(notifications, many=True)
        return Response(data={"results": serializer.data}, status=status.HTTP_200_OK)
