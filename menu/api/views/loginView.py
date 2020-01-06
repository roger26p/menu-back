from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
import requests
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from random import randint
from rest_framework_jwt.settings import api_settings
from rest_framework.authtoken.models import Token



class LoginView(APIView):
	permission_classes = (AllowAny,)    
	def post(self, request, format=None):

		l_error = []
		if 'user' not in request.data:
			l_error.append("Email requerido")
		if 'password' not in request.data:
			l_error.append("Password requerido")
		if len(l_error) > 0:
			return HttpResponse(JsonResponse({"error": l_error}),content_type="application/json", status=400)

		credentials = {"username": request.data["user"], "password": request.data["password"]}
		user = authenticate(**credentials)
		token = None

		if user:
			if not user.is_active:
				l_error.append("Usuario inactivo")
				return HttpResponse(JsonResponse({"error": l_error}),content_type="application/json", status=401)

			o_token, _ = Token.objects.get_or_create(user=user)
			token = o_token.key
		else:	
			token = 0

		return HttpResponse(JsonResponse({'token': token}),content_type="application/json", status=200)
