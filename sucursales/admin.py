from django.contrib import admin
from .models import Sucursal


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    """
    Admin configuration for Sucursal model
    """
    list_display = ('id', 'nombre', 'direccion', 'telefono', 'municipio', 'estado')
    list_filter = ('estado', 'municipio')
    search_fields = ('nombre', 'direccion', 'telefono')
    
    def municipio(self, obj):
        return obj.codigo_municipio.nombre_municipio
    municipio.short_description = 'Municipio'
