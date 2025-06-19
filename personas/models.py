# personas/models.py
from django.db import models
from core.models import Municipio

class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=20, unique=True)
    nombre_completo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    codigo_municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)

class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200)
    id_sucursal = models.ForeignKey('sucursales.Sucursal', on_delete=models.PROTECT)