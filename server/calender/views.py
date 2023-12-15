# views.py

import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.contrib.auth.models import User
from .models import Calendar, Event
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.middleware.csrf import get_token


@csrf_exempt
def CreateUser(request):
    params = json.loads(request.body)
    email = params['email']
    password = params['password']
    User.objects.create_user(username=email, email=email, password=password)
    return JsonResponse({'message': 'User created successfully'}, status=201)


@csrf_exempt
def Login(request):
    params = json.loads(request.body)
    email = params['email']
    password = params['password']
    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'}, status=201)
    else:
        return JsonResponse({'message': 'Login failed'}, status=401)


@csrf_exempt
def Logout(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})


@csrf_exempt
def DeleteUser(request):
    params = json.loads(request.body)
    email = params['email']
    user = User.objects.get(email=email)
    user.delete()
    return JsonResponse({'message': 'User deleted successfully'})


@csrf_exempt
def UpdateUser(request, username):
    user = User.objects.get(username=username)
    new_data = json.loads(request.body)
    user.email = new_data.get('email', user.email)
    user.username = username

    # パスワードの更新は set_password を使用
    password = new_data.get('password')
    if password:
        user.set_password(password)

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