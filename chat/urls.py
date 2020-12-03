from . import views
from django.urls import path
urlpatterns = [
    path('api/users/', views.UserListView.as_view(), name='user-list'),
    path('api/users/<int:pk>', views.UserDetailView.as_view(), name='user-instance'),
]
