from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, ValidationError

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

from hunchat.model_loaders import get_post_model, get_video_model

from posts.serializers import (
    PostSerializer,
    PostThreadSerializer,
)


class PostsViewset(
    ExternalIdViewMixin, SerializerExtensionsAPIViewMixin, viewsets.ReadOnlyModelViewSet
):
    """
    API endpoint that allows posts to be viewed.
    """

    queryset = get_post_model().objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


class PostCreateView(generics.UpdateAPIView):
    """
    API endpoint that allows posts to be created.
    """

    queryset = get_post_model().objects.all()
    serializer_class = PostSerializer
    parser_classes = [
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    ]

    def put(self, request):
        video = get_video_model().objects.create(
            file=request.data.get("file"),
            duration=float(request.data.get("duration")),
            height=int(request.data.get("height")),
            width=int(request.data.get("width")),
        )

        comment_to_hashid = request.data.get("comment_to", None)
        if comment_to_hashid:
            comment_to_id = internal_id_from_model_and_external_id(
                get_post_model(), comment_to_hashid
            )
            comment_to = get_post_model().objects.get(pk=comment_to_id)
            post = get_post_model().objects.create(
                description=request.data.get("description"),
                video=video,
                author=request.user,
                comment_to=comment_to,
            )
        else:
            post = get_post_model().objects.create(
                description=request.data.get("description"),
                video=video,
                author=request.user,
            )

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikePostView(generics.CreateAPIView):
    """
    API endpoint to like a post.
    """

    queryset = get_post_model().objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        pk = internal_id_from_model_and_external_id(get_post_model(), pk)
        post = get_post_model().objects.get(pk=pk)
        try:
            post_like = PostLike.objects.create(
                user=request.user,
                post=post,
            )
            post = get_post_model().objects.get(pk=pk)
            serializer = self.serializer_class(post)
            return Response(data={serializer.data}, status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response(
                data={"message": _("User already liked this post.")},
                status=status.HTTP_409_CONFLICT,
            )


class PostThreadView(generics.RetrieveAPIView):
    queryset = get_post_model().objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    # def get_queryset(self, pk):
    #     post = get_post_model().objects.get(pk=pk)
    #     return post.get_thread()

    def get(self, request, pk):
        pk = internal_id_from_model_and_external_id(get_post_model(), pk)
        thread = get_post_model().objects.get(pk=pk).get_thread()
        serializer = self.serializer_class(thread, many=True)
        return Response(serializer.data)
