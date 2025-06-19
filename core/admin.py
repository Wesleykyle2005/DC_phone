from django.contrib import admin
from .models import Municipio, Rol


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    """
    Admin configuration for Municipio model
    """
    list_display = ('codigo_municipio', 'nombre_municipio')
    search_fields = ('codigo_municipio', 'nombre_municipio')
    list_per_page = 20


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    """
    Admin configuration for Rol model
    """
    list_display = ('id_rol', 'nombre_rol')
    search_fields = ('id_rol', 'nombre_rol')
    list_per_page = 20

