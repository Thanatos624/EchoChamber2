from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    """
    Represents a blog post in the database.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # New field for the post's header image.
    # 'upload_to' specifies the subdirectory within your media folder.
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        """A string representation of the Post model, used in the admin panel."""
        return self.title

class Comment(models.Model):
    """
    Represents a comment on a blog post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """A string representation of the Comment model."""
        return f'Comment by {self.author.username} on "{self.post.title}"'


class UserPostInteraction(models.Model):
    """
    Records an interaction when a user views a post.
    This data is crucial for collaborative filtering.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures that each user-post pair is unique.
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.username} viewed "{self.post.title}"'
