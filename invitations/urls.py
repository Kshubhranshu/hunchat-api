from django.urls import path

from invitations import views


app_name = "invitations"

urlpatterns = [
    path("", views.InvitationView.as_view(), name="invitation"),
]
