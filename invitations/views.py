from django.shortcuts import render
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response

from invitations.serializers import InvitationSerializer


class InvitationView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
