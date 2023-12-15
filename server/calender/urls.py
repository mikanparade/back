# urls.py

from django.urls import path
from .views import CreateUser, Login, Logout, DeleteUser, UpdateUser, CalendarListView, EventDetailView, EventListView

urlpatterns = [
    path('api/users', CreateUser, name='create-user'),
    path('api/users/login', Login, name='login'),
    path('api/users/me/logout', Logout, name='logout'),
    path('api/users/me/delete', DeleteUser, name='delete-user'),
    path('api/users/<str:username>/update', UpdateUser, name='update-user'),
    path('api/calendars', CalendarListView.as_view(), name='calendar-list'),
    path('api/calendars/<int:calendar_id>/events', EventListView.as_view(), name='event-list'),
    path('api/calendars/<int:calendar_id>/events/<int:event_id>', EventDetailView.as_view(), name='event-detail'),
]
