from django.contrib import admin
from .models import Persona, Cliente, Empleado


class ClienteInline(admin.StackedInline):
    """
    Inline para Cliente en el admin de Persona
    """
    model = Cliente
    max_num = 1
    can_delete = False


class EmpleadoInline(admin.StackedInline):
    """
    Inline para Empleado en el admin de Persona
    """
    model = Empleado
    max_num = 1
    can_delete = False


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Persona
    """
    list_display = ('id_persona', 'dni', 'nombre_completo', 'telefono', 'codigo_municipio', 'estado')
    list_filter = ('estado', 'codigo_municipio')
    search_fields = ('dni', 'nombre_completo', 'telefono')
    list_per_page = 20
    inlines = [ClienteInline, EmpleadoInline]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editando un objeto existente
            return ['dni']
        return []


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Cliente
    """
    list_display = ('id_cliente', 'persona_info', 'telefono', 'municipio')
    search_fields = ('persona__dni', 'persona__nombre_completo')
    list_per_page = 20
    
    def persona_info(self, obj):
        return f"{obj.persona.nombre_completo} ({obj.persona.dni})"
    persona_info.short_description = 'Cliente'
    
    def telefono(self, obj):
        return obj.persona.telefono
    telefono.short_description = 'Teléfono'
    
    def municipio(self, obj):
        return obj.persona.codigo_municipio.nombre_municipio
    municipio.short_description = 'Municipio'


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Empleado
    """
    list_display = ('id_empleado', 'persona_info', 'direccion', 'sucursal', 'telefono', 'municipio')
    list_filter = ('id_sucursal',)
    search_fields = ('persona__dni', 'persona__nombre_completo', 'id_sucursal__nombre_sucursal', 'direccion')
    list_per_page = 20
    
    def persona_info(self, obj):
        return f"{obj.persona.nombre_completo} ({obj.persona.dni})"
    persona_info.short_description = 'Empleado'
    
    def telefono(self, obj):
        return obj.persona.telefono
    telefono.short_description = 'Teléfono'
    
    def municipio(self, obj):
        return obj.persona.codigo_municipio.nombre_municipio
    municipio.short_description = 'Municipio'
    
    def sucursal(self, obj):
        return obj.id_sucursal.nombre
    sucursal.short_description = 'Sucursal'

    def direccion(self, obj):
        return obj.direccion
    direccion.short_description = 'Dirección'
