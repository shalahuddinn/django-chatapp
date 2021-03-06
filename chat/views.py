from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.http import Http404
from django.http.response import JsonResponse
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from chat.models import Conversation, Message
from chat.serializers import UserSerializer, ConversationSerializer, MessageSerializer, ConversationSpecificUserSerializer, ModelUserSerializer, ModelMessageSerializer, ModelConversationSerializer


#  Use Case Scenario
class UserRegisterView(APIView):
    """
    Create a new user.
    """
    # Disable permission
    permission_classes = []

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['id'] = user.id
            data['username'] = user.username
            data['email'] = user.email
            token = Token.objects.get(user=user).key
            data['token'] = token
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConversationListSpecificUserView(APIView):
    """
    List of all of the conversations that a user participate
    """

    def get(self, request, format=None):
        user = self.request.user
        conversations = Conversation.objects.filter(participants=user)
        serializer = ConversationSpecificUserSerializer(
            conversations, context={'request': request}, many=True)
        return Response(serializer.data)


class ConversationCreateView(APIView):
    """
    Create a new conversation. User who made the request should be in the participants.
    """

    def post(self, request, format=None):
        serializer = ConversationSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageListCreateView(APIView):
    """
    List all messages in a particular conversation, or create a new message in a particular conversation.
    """

    def get(self, request, pk, format=None):
        # Check if the conversation with pk as the id exist
        try:
            conversation = Conversation.objects.get(id=pk)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation with that id doesn't exist"})

        # Check if the user is a participant in the conversation
        participants = conversation.participants.all()
        user = self.request.user
        if user not in participants:
            return Response({"error": "User is not a participant in this conversation"})

        # Update all unread messages is_read field as True if the user who made the get request are not the sender
        unread_messages = Message.objects.filter(
            ~Q(sender=user), conversation_id=pk, is_read=False)
        print(f'unread_message: {unread_messages}')
        for message in unread_messages:
            message.is_read = True
            message.save()

        messages = Message.objects.filter(conversation_id=pk)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        # Check if the conversation with pk as the id exist
        try:
            conversation = Conversation.objects.get(id=pk)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation with that id doesn't exist"})

        # Check if the user is a participant in the conversation
        participants = conversation.participants.all()
        user = self.request.user
        if user not in participants:
            return Response({"error": "Can't send a message. User is not a participant in this conversation"})

        # Check if the request.data has message field
        try:
            data = {
                "conversation_id": pk,
                "sender": self.request.user.username,
                "message": request.data["message"]
            }
        except:
            return Response({"message": [
                "This field is required."
            ]})

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Model Data Manipulation
class ModelUserViewset(viewsets.ModelViewSet):
    """
    Retrieve, create, update or delete a user model.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = ModelUserSerializer


class ModelMessageViewset(viewsets.ModelViewSet):
    """
    Retrieve, create, update or delete a Message model.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Message.objects.all()
    serializer_class = ModelMessageSerializer


class ModelConversationViewset(viewsets.ModelViewSet):
    """
    Retrieve, create, update or delete a Conversation model.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Conversation.objects.all()
    serializer_class = ModelConversationSerializer
