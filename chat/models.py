from django.db import models
# Importing User Model
from django.contrib.auth.models import User


# Create your models here.
class Conversation(models.Model):
    participants = models.ManyToManyField(User)


class Message(models.Model):
    conversation_id = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='message')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)


# class UserConversation(models.Model):
#     user_id = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='user')
#     conversation_id = models.ForeignKey(
#         Conversation, on_delete=models.CASCADE, related_name='conversation')
