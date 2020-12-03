from django.contrib import admin
from chat.models import Conversation, Message, UserConversation

# Register your models here.
admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(UserConversation)
