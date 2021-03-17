from rest_framework import serializers

from hunchat.model_loaders import get_video_model


class VideoSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    poster_url = serializers.SerializerMethodField()

    class Meta:
        model = get_video_model()
        fields = [
            "id",
            "file",
            "file_url",
            "duration",
            "height",
            "width",
            "poster",
            "poster_url",
            "poster_height",
            "poster_width",
        ]

    def get_file_url(self, obj):
        file = obj.file
        if file:
            return file.url
        return None

    def get_poster_url(self, obj):
        poster = obj.poster
        if poster:
            return poster.url
        return None
