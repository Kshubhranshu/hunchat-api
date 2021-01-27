from django.apps import apps


def get_video_comment_notification_model():
    return apps.get_model("notifications.VideoCommentNotification")


def get_video_model():
    return apps.get_model("videos.Video")
