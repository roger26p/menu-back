from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
import requests
from django.contrib.auth.models import User
from api.models.menuModel import *
from datetime import datetime, timedelta
from random import randint
from rest_framework_jwt.settings import api_settings
from rest_framework.authtoken.models import Token

class MenuView(APIView):
	permission_classes = (AllowAny,)    

	def get(self, request, format=None):
		array_menu = []
		menu = Menu.objects.all().order_by('date_created')
		for m in menu:
			array_menu.append(m.get())
		return HttpResponse(JsonResponse({"menu": array_menu}),content_type="application/json", status=200)

	def post(self, request, format=None):
		accion = None
		nombre = request.data["nombre"]
		descripcion = request.data["descripcion"]
		fecha = request.data["fecha"]
		fecha = datetime.strptime(fecha, "%Y-%m-%d")

		consulta_menu = Menu.objects.filter(Q(nombre=nombre.upper(), date_created=fecha))
		if len(consulta_menu) == 0:
			menu = Menu.objects.create(
				nombre=nombre.upper(),  
				descripcion=descripcion,
				date_created=fecha
			)
			menu.save()
			accion = "Menú creado"
		else:
			consulta_menu.update(
				nombre=nombre.upper(),  
				descripcion=descripcion
			)	
			accion = "Menú actualizado"

		return HttpResponse(JsonResponse({"accion": accion}),content_type="application/json", status=200)

	def put(self, request, format=None):
		accion = None
		id_menu = request.data["id_menu"]
		nombre = request.data["nombre"]
		descripcion = request.data["descripcion"]
		fecha = request.data["fecha"]
		fecha = datetime.strptime(fecha, "%Y-%m-%d")

		consulta_menu = Menu.objects.filter(Q(id=int(id_menu)))
		if len(consulta_menu) == 0:
			menu = Menu.objects.create(
				nombre=nombre.upper(),  
				descripcion=descripcion,
				date_created=fecha
			)
			menu.save()
			accion = "Menú creado"
		else:
			consulta_menu.update(
				nombre=nombre.upper(),  
				descripcion=descripcion,
				date_created=fecha
			)	
			accion = "Menú actualizado"

		return HttpResponse(JsonResponse({"accion": accion}),content_type="application/json", status=200)

	def delete(self, request, pk, format=None):
		menu = Menu.objects.filter(Q(id=pk))
		if len(menu) == 0:
			return HttpResponse(JsonResponse({"error": 'El menú no existe.'}),content_type="application/json", status=400)
		else:
			menu.delete()	

		return HttpResponse(JsonResponse({"accion": 'Menú eliminado.'}), content_type="application/json", status=200)		

class MenuIndividualView(APIView):
	permission_classes = (AllowAny,)    

	def get(self, request, pk, format=None):
		obje=None
		l_error = []
		
		try:
			menu = Menu.objects.get(id=pk)
			obje = {"id": menu.id, "nombre": menu.nombre, "descripcion": menu.descripcion, "fecha": menu.date_created}
		except Menu.DoesNotExist:
			return HttpResponse(JsonResponse({"error": l_error}),content_type="application/json", status=400)

		return HttpResponse(JsonResponse({"menu": obje}),content_type="application/json", status=200)

class PedidosView(APIView):
	permission_classes = (AllowAny,) 

	def get(self, request, format=None):
		array_pedidos = []
		date = datetime.utcnow()
		pedidos = Pedidos.objects.filter(Q(date_created=date))
		for p in pedidos:
			obje=None
			try:
				menu = Menu.objects.get(id=p.menu_id)
				obje = {"nombre": menu.nombre, "descripcion": menu.descripcion}
			except Menu.DoesNotExist:
				return HttpResponse(JsonResponse({"error": l_error}),content_type="application/json", status=400)

			obje['extra']=p.extra

			array_pedidos.append(obje)
		return HttpResponse(JsonResponse({"pedidos": array_pedidos}),content_type="application/json", status=200)

	def post(self, request, format=None):
		accion = None
		extra = request.data["extra"]
		id_menu = request.data["id_menu"]
		date = datetime.utcnow()

		consulta_pedido = Pedidos.objects.filter(Q(user_id=request.user.id, date_created=date))
		if len(consulta_pedido) == 0:
			pedido = Pedidos.objects.create(
				extra=extra,
				date_created=date,
				menu_id=id_menu,
				user_id=request.user.id
			)
			pedido.save()
			accion = "Pedido creado"
		else:
			accion = "Ya realizaste un pedido hoy."

		return HttpResponse(JsonResponse({"accion": accion}),content_type="application/json", status=200)