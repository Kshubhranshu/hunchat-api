from rest_framework import serializers

from hunchat.model_loaders import get_video_model


class VideoSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = get_video_model()
        fields = ["id", "file", "file_url", "duration", "height", "width"]

    def get_file_url(self, obj):
        file = obj.file
        if file:
            return file.url
        return None
