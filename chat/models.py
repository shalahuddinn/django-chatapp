from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.
class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversation")


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


# Auto generate Token for a new created user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Make the email field as required field in the user model
User._meta.get_field('email').blank = False
