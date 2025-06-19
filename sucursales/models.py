# sucursales/models.py
from django.db import models
from core.models import Municipio

class Sucursal(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre