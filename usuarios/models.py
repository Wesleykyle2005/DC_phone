# usuarios/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from personas.models import Empleado
from core.models import Rol

# class Usuario(AbstractUser):
#     id_empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE, null=True, blank=True)
#     id_rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True)
#     estado = models.BooleanField(default=True, null=True, blank=True)