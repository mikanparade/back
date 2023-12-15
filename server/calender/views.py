# views.py

import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.contrib.auth.models import User
from .models import Calendar, Event

@method_decorator(csrf_exempt, name='dispatch')
class CreateUserAPIView(View):

    def post(self, request):
        params = json.loads(request.body)
        email = params['email']
        password = params['password']
        User.objects.create_user(username=email, email=email, password=password)
        return JsonResponse({'message': 'User created successfully'}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(View):

    def post(self, request, email):
        params = json.loads(request.body)
        password = params['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=201)
        else:
            return JsonResponse({'message': 'Login failed'}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutAPIView(View):

    def delete(self, request, user_id):
        logout(request)
        return JsonResponse({'message': 'Logout successful'})


@method_decorator(csrf_exempt, name='dispatch')
class DeleteUserAPIView(View):

    def delete(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'})


@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserAPIView(View):

    def put(self, request, user_id):
        user = User.objects.get(pk=user_id)
        new_data = json.loads(request.body)
        user.email = new_data.get('email', user.email)
        user.password = new_data.get('password', user.password)
        user.save()
        return JsonResponse({'message': 'User updated successfully'})

@method_decorator(csrf_exempt, name='dispatch')
class CalendarListView(View):
    def get(self, request):
        # リクエストしてきたユーザーが持っているカレンダーの一覧を取得
        user_calendars = Calendar.objects.filter(user=request.user)
        calendars_data = [{'id': calendar.id, 'name': calendar.name} for calendar in user_calendars]
        return JsonResponse(calendars_data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class EventListView(View):
    def get(self, request, calendar_id):
        try:
            # カレンダーが存在するか確認
            calendar = Calendar.objects.get(id=calendar_id, user=request.user)
            # カレンダーに関連するイベントを取得
            events_data = [{'id': event.id, 'summary': event.summary, 'start': event.start, 'end': event.end} for event in calendar.events.all()]
            return JsonResponse(events_data, safe=False)
        except Calendar.DoesNotExist:
            return JsonResponse({'message': 'Calendar not found'}, status=404)

    def post(self, request, calendar_id):
        try:
            # カレンダーが存在するか確認
            calendar = Calendar.objects.get(id=calendar_id, user=request.user)
            # リクエストデータを使ってイベントを作成
            data = json.loads(request.body)
            event = Event.objects.create(calendar=calendar, **data)
            return JsonResponse({'id': event.id, 'message': 'Event created successfully'}, status=201)
        except Calendar.DoesNotExist:
            return JsonResponse({'message': 'Calendar not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class EventDetailView(View):
    def put(self, request, calendar_id, event_id):
        try:
            # カレンダーが存在するか確認
            calendar = Calendar.objects.get(id=calendar_id, user=request.user)
            # イベントが存在するか確認
            event = Event.objects.get(id=event_id, calendar=calendar)
            # リクエストデータを使ってイベントを更新
            data = json.loads(request.body)
            calendar.to_updated(data).save()
            return JsonResponse({'message': 'Event updated successfully'}, status=204)
        except Calendar.DoesNotExist:
            return JsonResponse({'message': 'Calendar not found'}, status=404)
        except Event.DoesNotExist:
            return JsonResponse({'message': 'Event not found'}, status=404)