from django.apps import apps


def get_notification_model():
    return apps.get_model("notifications.Notification")


def get_post_comment_notification_model():
    return apps.get_model("notifications.PostCommentNotification")


def get_post_like_notification_model():
    return apps.get_model("notifications.PostLikeNotification")


def get_post_model():
    return apps.get_model("posts.Post")


def get_post_like_model():
    return apps.get_model("posts.PostLike")


def get_video_model():
    return apps.get_model("videos.Video")
