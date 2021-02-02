from django import forms

from invitations.models import Invitation


class InvitationForm(forms.Form):
    email = forms.EmailField()

    class Meta:
        model = Invitation
        fields = ["email"]
