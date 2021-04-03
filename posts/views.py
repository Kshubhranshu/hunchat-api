from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import (
    filters,
    generics,
    mixins,
    parsers,
    permissions,
    status,
    viewsets,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_serializer_extensions.utils import (
    internal_id_from_model_and_external_id,
)
from rest_framework_serializer_extensions.views import (
    ExternalIdViewMixin,
    SerializerExtensionsAPIViewMixin,
)

from hunchat.model_loaders import get_post_like_model, get_post_model, get_video_model
from posts.serializers import PostSerializer, PostThreadSerializer


class PostsViewSet(
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

    def create(self, request, pk=None):
        pk = internal_id_from_model_and_external_id(get_post_model(), pk)
        post = get_post_model().objects.get(pk=pk)
        try:
            get_post_like_model().objects.create(
                user=request.user,
                post=post,
            )
            post = get_post_model().objects.get(pk=pk)
            serializer = self.serializer_class(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response(
                {"message": _("User already liked this post.")},
                status=status.HTTP_409_CONFLICT,
            )


class PostThreadView(generics.RetrieveAPIView):
    queryset = get_post_model().objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        pk = internal_id_from_model_and_external_id(get_post_model(), pk)
        thread = get_post_model().objects.get(pk=pk).get_thread()
        serializer = self.serializer_class(thread, many=True)
        return Response(serializer.data)


class PostCommentsView(generics.RetrieveAPIView):
    queryset = get_post_model().objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        pk = internal_id_from_model_and_external_id(get_post_model(), pk)
        comments = get_post_model().objects.get(pk=pk).get_comments()
        serializer = self.serializer_class(comments, many=True)
        return Response({"results": serializer.data})


class UserPostsView(generics.ListAPIView):
    """
    API endpoint to get user posts.
    """

    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Get user's posts."""
        pk = self.kwargs["pk"]
        pk = internal_id_from_model_and_external_id(get_user_model(), pk)
        user = get_user_model().objects.get(pk=pk)
        posts = user.posts
        return posts

    def get(self, request, *args, **kwargs):
        """Get user posts by user external id."""
        try:
            posts = self.get_queryset()
            serializer = self.serializer_class(posts, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(
                {"message": "No user exists with that id."},
                status=status.HTTP_404_NOT_FOUND,
            )
