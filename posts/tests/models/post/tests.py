from django.test import TestCase

from posts.models import Post, PostLike


class PostTests(TestCase):
    fixtures = ["users.json", "videos.json", "posts.json", "post_likes.json"]

    def test_get_comments(self):
        """
        Ensure we can get the comments of a post.
        """
        post = Post.objects.get(pk=1)
        comments = post.get_comments()

        self.assertQuerysetEqual(
            comments.all(), [repr(Post.objects.get(pk=6)), repr(Post.objects.get(pk=2))]
        )

    def test_get_comments_count(self):
        """
        Ensure we can get the number of comments of a post.
        """
        post = Post.objects.get(pk=1)
        comments_count = post.get_comments_count()

        self.assertEqual(comments_count, 2)

    def test_get_likes(self):
        """
        Ensure we can get the likes of a post.
        """
        post = Post.objects.get(pk=1)
        likes = post.get_likes()

        self.assertQuerysetEqual(
            likes.all(),
            [repr(PostLike.objects.get(pk=1)), repr(PostLike.objects.get(pk=3))],
            ordered=False,
        )

    def test_get_likes_count(self):
        """
        Ensure we can get the number of likes of a post.
        """
        post = Post.objects.get(pk=1)
        likes_count = post.get_likes_count()

        self.assertEqual(likes_count, 2)

    def test_get_thread_post_when_post_is_comment(self):
        """
        Ensure we can get the thread of a post with non-null comment_to field.
        """
        post = Post.objects.get(pk=7)
        thread = post.get_thread()

        self.assertEqual(
            thread,
            [
                Post.objects.get(pk=1),
                Post.objects.get(pk=2),
                Post.objects.get(pk=4),
                Post.objects.get(pk=7),
            ],
        )

    def test_get_thread_post_when_post_is_not_comment(self):
        """
        Ensure we can get the thread of a post with null comment_to field.
        """
        post = Post.objects.get(pk=8)
        thread = post.get_thread()

        self.assertEqual(thread, None)
