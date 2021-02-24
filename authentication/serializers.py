from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as JWTTokenObtainPairSerializer,
)

from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from rest_framework_serializer_extensions.fields import HashIdField
from rest_framework_serializer_extensions.utils import (
    external_id_from_model_and_internal_id,
)

from hunchat.model_loaders import get_video_model

from authentication.validators import (
    username_characters_validator,
    username_not_taken_validator,
    email_not_taken_validator,
    user_email_exists,
)

from videos.serializers import VideoSerializer


class UserBaseSerializer(
    SerializerExtensionsMixin, serializers.HyperlinkedModelSerializer
):
    id = HashIdField(model=get_user_model(), read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "name",
            "email",
            "password",
            "are_terms_accepted",
            "is_newsletter_subscribed",
        ]
        read_only_fields = [
            "id",
        ]

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise ValidationError(str(exc))
        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = get_user_model()(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user


class UserSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    """User serializer"""

    id = HashIdField(model=get_user_model(), read_only=True)
    image_url = serializers.SerializerMethodField()
    bio_video = VideoSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "name",
            "email",
            "image",
            "image_url",
            "bio",
            "bio_video",
            "location",
            "date_joined",
            "link",
        ]

    def get_image_url(self, obj):
        image = obj.image
        if image:
            return image.url
        return None


class UserBioVideoSerializer(serializers.ModelSerializer):
    id = HashIdField(model=get_user_model(), read_only=True)
    bio_video = VideoSerializer()

    class Meta:
        model = get_user_model()
        fields = ["id", "bio_video"]

    # def validate(self, data):
    #     print('DATA', data)
    #
    # def update(self, instance, validated_data):
    #     print('VALIDATED DATA', validated_data)
    # video = get_video_model().objects.create(**validated_data)
    # instance.bio_video = video
    # instance.save()
    # return instance


class UsernameCheckSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[username_characters_validator, username_not_taken_validator],
    )


class EmailCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        validators=[EmailValidator, email_not_taken_validator],
    )


class TokenPairSerializer(JWTTokenObtainPairSerializer):
    """Token pair serializer."""

    @classmethod
    def get_token(cls, user):
        """Includes user hashid in token."""
        token = super().get_token(user)
        hashid = external_id_from_model_and_internal_id(get_user_model(), user.id)
        token["user_hashid"] = hashid
        return token


class CheckRefreshTokenIsBlacklistedSerializer(serializers.Serializer):
    """Refresh token serializer to check if refresh token is blacklisted"""

    jti = serializers.CharField()
