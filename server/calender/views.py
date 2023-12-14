# views.py

import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.contrib.auth.models import User

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
