from django.contrib.auth.models import User
from rest_framework import serializers
from chat.models import Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'], validated_data['password']
                                        )
        return user


class ConversationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                      many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation_id', 'sender',
                  'message', 'timestamp', 'is_read']
