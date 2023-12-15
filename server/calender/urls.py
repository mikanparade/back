# urls.py

from django.urls import path
from .views import CreateUserAPIView, LoginAPIView, LogoutAPIView, DeleteUserAPIView, UpdateUserAPIView, CalendarListView, EventDetailView, EventListView

urlpatterns = [
    path('api/users', CreateUserAPIView.as_view(), name='create-user'),
    path('api/users/<str:email>/sessions', LoginAPIView.as_view(), name='login'),
    path('api/users/<int:user_id>/sessions/current', LogoutAPIView.as_view(), name='logout'),
    path('api/users/<int:user_id>', DeleteUserAPIView.as_view(), name='delete-user'),
    path('api/users/<int:user_id>', UpdateUserAPIView.as_view(), name='update-user'),
    path('api/calendars', CalendarListView.as_view(), name='calendar-list'),
    path('api/calendars/<int:calendar_id>/events', EventListView.as_view(), name='event-list'),
    path('api/calendars/<int:calendar_id>/events/<int:event_id>', EventDetailView.as_view(), name='event-detail'),
]
