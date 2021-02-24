from django.urls import include, path

from rest_framework import routers

from authentication import views


app_name = "authentication"

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "users/<str:pk>/bio_video/",
        views.UserBioVideoView.as_view(),
        name="users_detail_bio_video",
    ),
    path(
        "users/<str:pk>/image/",
        views.UserImageView.as_view(),
        name="users_detail_image",
    ),
    path(
        "auth/username_available/",
        views.UsernameAvailableView.as_view(),
        name="username_available",
    ),
    path(
        "auth/email_available/",
        views.EmailAvailableView.as_view(),
        name="email_available",
    ),
    path(
        "auth/token/obtain/",
        views.TokenObtainPairView.as_view(),
        name="token_create",
    ),
    path("auth/token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "auth/token/check/",
        views.CheckRefreshTokenIsBlacklistedView.as_view(),
        name="token_check",
    ),
    path(
        "auth/token/blacklist/",
        views.BlacklistRefreshTokenView.as_view(),
        name="blacklist",
    ),
]
