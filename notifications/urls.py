from django.urls import path

from notifications import views

app_name = "notifications"


urlpatterns = [
    path(
        "users/<str:pk>/notifications/",
        views.NotificationsView.as_view(),
        name="user_notifications",
    ),
]
