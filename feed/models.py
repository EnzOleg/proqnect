from django.db import models
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(verbose_name="Содержимое поста")
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    like_count = models.PositiveIntegerField(default=0) 

    def update_like_count(self):
        self.like_count = self.likes.count()
        self.save(update_fields=["like_count"])  

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()

    def __str__(self):
        return f"Пост {self.user.email} от {self.created_at:%d.%m.%Y %H:%M}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_user_post_like")
        ]

    def __str__(self):
        return f"{self.user.email} лайкнул пост {self.post.id}"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="replies", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} комментирует {self.post.id}: {self.content[:30]}..."
    
    @property
    def top_parent(self):
        if self.parent is None:
            return self
        return self.parent.top_parent
