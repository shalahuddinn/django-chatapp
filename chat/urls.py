from . import views
from django.urls import path
urlpatterns = [
    path('api/users/', views.UserListView.as_view(), name='user-list'),
    path('api/users/<int:pk>', views.UserDetailView.as_view(), name='user-instance'),
    path('api/conversations/', views.ConversationListView.as_view(),
         name='conversation-list'),
    path('api/conversations/users/<int:pk>', views.ConversationListSpecificUserView.as_view(),
         name='conversation-list-specific-user'),
    path('api/conversations/<int:pk>', views.ConversationDetailView.as_view(),
         name='conversation-detail'),
    path('api/conversations/<int:pk>/messages', views.MessageListView.as_view(),
         name='conversation-detail'),
]
