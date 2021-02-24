from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import (
    generics,
    mixins,
    permissions,
    viewsets,
    status,
    filters,
    parsers,
)
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_serializer_extensions.views import (
    ExternalIdViewMixin,
    SerializerExtensionsAPIViewMixin,
)
from rest_framework_serializer_extensions.utils import (
    internal_id_from_model_and_external_id,
)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView as JWTTokenObtainPairView,
    TokenRefreshView as JWTTokenRefreshView,
)
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer as JWTTokenRefreshSerializer,
)
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from hunchat import permissions as hunchat_permissions
from hunchat.model_loaders import get_video_model

from authentication.serializers import (
    UserBaseSerializer,
    UserSerializer,
    UserBioVideoSerializer,
    UsernameCheckSerializer,
    EmailCheckSerializer,
    TokenPairSerializer,
    CheckRefreshTokenIsBlacklistedSerializer,
)


class UserViewSet(
    ExternalIdViewMixin, SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet
):
    """
    API endpoint that allows users to be viewed, created, edited or deleted.
    """

    search_fields = ["username", "name"]
    filter_backends = [
        filters.SearchFilter,
    ]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        """
        Override permissions for DELETE, PUT and PATCH HTTP methods: only admin
        or instance user can access.
        """
        require_admin_or_self_access = ["destroy", "update", "partial_update"]
        if self.action in require_admin_or_self_access:
            return [
                hunchat_permissions.IsAdminOrIsSelf(),
            ]
        return super(UserViewSet, self).get_permissions()

    def create(self, request, format="json"):
        serializer = UserBaseSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBioVideoView(
    ExternalIdViewMixin,
    SerializerExtensionsAPIViewMixin,
    generics.UpdateAPIView,
):
    queryset = get_user_model().objects.all()
    serializer_class = UserBioVideoSerializer
    parser_classes = [
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    ]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        video = get_video_model().objects.create(
            file=request.data.get("file"),
            duration=float(request.data.get("duration")),
            height=int(request.data.get("height")),
            width=int(request.data.get("width")),
        )

        instance.bio_video = video
        instance.save()

        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class UserImageView(
    ExternalIdViewMixin,
    SerializerExtensionsAPIViewMixin,
    generics.UpdateAPIView,
):
    queryset = get_user_model().objects.all()
    parser_classes = [
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    ]

    def put(self, request, *args, **kwargs):
        user_hashid = kwargs["pk"]
        user_id = internal_id_from_model_and_external_id(get_user_model(), user_hashid)
        file = request.FILES.get("file")
        if file:
            user = get_user_model().objects.get(pk=user_id)
            user.image = file
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "No image file detected."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UsernameAvailableView(APIView):
    """
    API endpoint to check if a username is both valid and not taken.
    """

    serializer_class = UsernameCheckSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"username": _("Username available.")}, status=status.HTTP_202_ACCEPTED
        )


class EmailAvailableView(APIView):
    """
    API endpoint to check if an email is both valid and not taken.
    """

    serializer_class = EmailCheckSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"email": _("Email available.")}, status=status.HTTP_202_ACCEPTED
        )


class TokenObtainPairView(JWTTokenObtainPairView):
    """View that returns user hashid with token pair"""

    serializer_class = TokenPairSerializer


class TokenRefreshView(JWTTokenRefreshView):
    """
    Takes a refresh token and returns a new access token
    """

    serializer_class = JWTTokenRefreshSerializer


class CheckRefreshTokenIsBlacklistedView(APIView):
    """
    API endpoint to check if a refresh token is blacklisted.
    """

    serializer_class = CheckRefreshTokenIsBlacklistedSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                blacklisted_token = BlacklistedToken.objects.get(
                    token__jti=serializer.data["jti"]
                )
                return Response(data={"message": _("Refresh token is blacklisted")})
        except ObjectDoesNotExist:
            return Response(data={"message": _("Refresh token is not blacklisted")})


class BlacklistRefreshTokenView(APIView):
    """
    API endpoint to blacklist refresh token.
    """

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
