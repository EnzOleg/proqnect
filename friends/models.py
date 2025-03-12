from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Friendship(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "friend"]

    def __str__(self):
        return f"self.user.first_name дружит с self.friend.first_name"
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="sent_requests")
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="received_requests")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"