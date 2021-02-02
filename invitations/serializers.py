from rest_framework import serializers

from invitations.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    """Invitation serializer."""

    class Meta:
        model = Invitation
        fields = ["email"]
