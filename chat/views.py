from django.shortcuts import render
from django.http import Http404
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
# from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from chat.models import Conversation, Message
from chat.serializers import UserSerializer, ConversationSerializer, MessageSerializer, ConversationSpecificUserSerializer

# Create your views here.


class MessageListView(APIView):
    """
    List all messages in a conversation, or create a new message in a conversation.
    """

    def get_object(self, pk):
        try:
            return Message.objects.filter(conversation_id=pk)
        except Message.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        messages = self.get_object(pk)
        serializer = MessageSerializer(messages, many=True)
        print(f'user: {request.user}')
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConversationListSpecificUserView(APIView):
    """
    List all conversations for a specific user
    """

    def get(self, request, format=None):
        user = self.request.user
        conversations = Conversation.objects.filter(participants=user)
        serializer = ConversationSpecificUserSerializer(
            conversations, many=True)
        return Response(serializer.data)


class ConversationListView(APIView):
    """
    List all conversations, or create a new conversation.
    """

    def get(self, request, format=None):
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(
            conversations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # print(request.data)
        serializer = ConversationSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConversationDetailView(APIView):
    """
    Retrieve, update or delete a conversation instance.
    """

    def get_object(self, pk):
        try:
            return Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        conversation = self.get_object(pk)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)


class UserListView(APIView):
    """
    List all users, or create a new user.
    """

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(
            users, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(APIView):
    """
    Create a new user.
    """
    # Disable authentication
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
            # return Response(data)
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    Retrieve, update or delete a user instance.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
