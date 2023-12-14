# urls.py

from django.urls import path
from .views import CreateUserAPIView, LoginAPIView, LogoutAPIView, DeleteUserAPIView, UpdateUserAPIView

urlpatterns = [
    path('api/users', CreateUserAPIView.as_view(), name='create-user'),
    path('api/users/<str:email>/sessions', LoginAPIView.as_view(), name='login'),
    path('api/users/<int:user_id>/sessions/current', LogoutAPIView.as_view(), name='logout'),
    path('api/users/<int:user_id>', DeleteUserAPIView.as_view(), name='delete-user'),
    path('api/users/<int:user_id>', UpdateUserAPIView.as_view(), name='update-user'),
]
