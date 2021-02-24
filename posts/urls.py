from django.urls import include, path

from rest_framework import routers

from posts import views


app_name = "posts"

router = routers.DefaultRouter()
router.register(r"posts", views.PostsViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("posts_create/", views.PostCreateView.as_view(), name="posts_create"),
    path("posts/<str:pk>/like/", views.LikePostView.as_view(), name="posts_like"),
    path("posts/<str:pk>/thread/", views.PostThreadView.as_view(), name="posts_thread"),
]
