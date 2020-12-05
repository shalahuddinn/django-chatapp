from django.contrib.auth.models import User
from django.db.models import Q
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


class LastMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message', 'timestamp']


class ConversationSpecificUserSerializer(serializers.ModelSerializer):
    participants = ConversationUserSerializer(many=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'participants', 'last_message', 'unread_count']

    def get_user_from_request(self):
        request = self.context.get('request')
        # print(f'request: {request}')
        if not request:
            return None
        if not hasattr(request, 'user'):
            return None
        return request.user

    def get_last_message(self, obj):
        try:
            last_message = Message.objects.filter(
                conversation_id=obj.id).latest('timestamp')
            serializer = LastMessageSerializer(instance=last_message)
            return serializer.data
        except:
            last_message = None
            return last_message

    def get_unread_count(self, obj):
        user = self.get_user_from_request()
        try:
            unread_message_count = Message.objects.filter(
                ~Q(sender=user), conversation_id=obj.id, is_read=False).count()
            print(f'unread_count:{unread_message_count}')
            return unread_message_count
        except Message.DoesNotExist:
            unread_message_count = 0
            return unread_message_count


class ConversationSerializer(serializers.ModelSerializer):
    # participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
    #                                                   many=True)
    participants = serializers.SlugRelatedField(
        queryset=User.objects.all(), many=True,
        slug_field='username'
    )

    class Meta:
        model = Conversation
        fields = ['id', 'participants']

    def get_user_from_request(self):
        request = self.context.get('request')
        # print(f'request: {request}')
        if not request:
            return None
        if not hasattr(request, 'user'):
            return None
        return request.user

    def validate_participants(self, value):
        """
        Check that the participants doesn't exist in conversation.
        """
        if len(value) < 2:
            raise serializers.ValidationError(
                "Participants should be 2 users. Format: [<username1>, <username2>] ")

        if len(value) > 2:
            raise serializers.ValidationError(
                "Maximum Participants: 2")

        if value[0] == value[1]:
            raise serializers.ValidationError(
                "Participant 1 and Participant 2 can't be from the same user")

        user = self.get_user_from_request()
        # print(f'user: {user}')
        # print(f'value[0]: {value[0]}')
        # print(f'value[1]: {value[1]}')
        if user not in value:
            raise serializers.ValidationError('User must be in participants.')

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
    sender = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Message
        fields = ['id', 'conversation_id', 'sender',
                  'message', 'timestamp', 'is_read']
