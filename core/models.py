# core/models.py
from django.db import models

class Municipio(models.Model):
    codigo_municipio = models.CharField(max_length=10, primary_key=True)
    nombre_municipio = models.CharField(max_length=50)

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)