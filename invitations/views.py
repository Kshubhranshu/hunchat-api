from django.shortcuts import render

from rest_framework import status, permissions, mixins, generics
from rest_framework.response import Response

from invitations.serializers import InvitationSerializer


class InvitationView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
