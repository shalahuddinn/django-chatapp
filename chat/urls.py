from . import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/users/', views.UserListView.as_view(), name='user-list'),
    #     path('api/users/<int:pk>', views.UserDetailView.as_view(), name='user-instance'),
    path('api/users/register/',
         views.UserRegisterView.as_view(), name='user-register'),
    path('api/users/login/', obtain_auth_token, name='user-login'),
    #     path('api/conversations/', views.ConversationListView.as_view(),
    #          name='conversation-list'),
    path('api/conversations/users/', views.ConversationListSpecificUserView.as_view(),
         name='conversation-list-specific-user'),
    path('api/conversations/', views.ConversationView.as_view(),
         name='conversation'),
    path('api/conversations/<int:pk>/messages/', views.MessageListView.as_view(),
         name='conversation-detail'),
]
