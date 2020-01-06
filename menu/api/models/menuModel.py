from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class Menu(models.Model):
	nombre=models.CharField(max_length=100, default=None, null=True)
	descripcion=models.CharField(max_length=1000, default=None, null=True)
	date_created=models.DateField(blank=True, null=True)

	def get(self):
		obj = {
			"id": self.id, 
			"nombre": self.nombre, 
			"descripcion": self.descripcion, 
			"date_created": self.date_created
		}

		return obj

class Pedidos(models.Model):
	user=models.ForeignKey(User, null=True, default=None, related_name='pedidos_user', on_delete=models.CASCADE)
	menu=models.ForeignKey(Menu, null=True, default=None, related_name='pedidos_menu', on_delete=models.CASCADE)
	extra=models.CharField(max_length=1000, default=None, null=True)	
	date_created=models.DateField(blank=True, null=True)

	def get(self):
		obj = {
			"id": self.id, 
			"user": self.user_id, 
			"menu": self.menu_id, 
			"extra": self.extra, 
			"date_created": self.date_created
		}

		return obj