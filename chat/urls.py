from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# Model/data Manipulation URL
router = DefaultRouter()
router.register(r'data/user', views.ModelUserViewset)
router.register(r'data/message', views.ModelMessageViewset)
router.register(r'data/conversation', views.ModelConversationViewset)

urlpatterns = [
    # Model/data Manipulation
    path('', include(router.urls)),

    # Use case scenario
    path('api/user/register/',
         views.UserRegisterView.as_view(), name='user-register'),
    path('api/user/login/', obtain_auth_token, name='user-login'),
    path('api/conversation/user/', views.ConversationListSpecificUserView.as_view(),
         name='conversation-list-specific-user'),
    path('api/conversation/create/', views.ConversationCreateView.as_view(),
         name='conversation'),
    path('api/conversation/<int:pk>/message/', views.MessageListCreateView.as_view(),
         name='conversation-detail'),
]
