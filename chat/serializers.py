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


class ConversationSpecificUserSerializer(serializers.ModelSerializer):
    participants = ConversationUserSerializer(many=True)
    last_message = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ['id', 'participants', 'last_message']


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                      many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants']

    def validate_participants(self, value):
        """
        Check that the participants doesn't exist in conversation.
        """
        if len(value) > 2:
            raise serializers.ValidationError(
                "Maximum Participants: 2")

        query1 = Conversation.objects.filter(participants=value[0])
        # print(f'Query1: {query1}')
        query2 = Conversation.objects.filter(participants=value[1])
        # print(f'Query2: {query2}')

        # print(f'Query Intersection: {query1.intersection(query2)}')
        if query1.intersection(query2).exists():
            raise serializers.ValidationError(
                "Conversation with these participants has exist")
        return value


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation_id', 'sender',
                  'message', 'timestamp', 'is_read']
