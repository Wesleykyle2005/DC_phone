from django.contrib import admin
from .models import Factura, DetalleFactura


class DetalleFacturaInline(admin.TabularInline):
    """
    Inline para DetalleFactura en el admin de Factura
    """
    model = DetalleFactura
    extra = 1
    readonly_fields = ('subtotal',)
    fields = ('id_producto', 'cantidad', 'precio_unitario', 'subtotal')


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Factura
    """
    list_display = (
        'id_factura',
        'id_cliente',
        'id_empleado',
        'id_sucursal',
        'fecha',
        'total',
        'estado'
    )
    list_filter = ('estado', 'id_sucursal', 'id_empleado')
    search_fields = (
        'id_factura',
        'id_cliente__nombre',
        'id_empleado__nombre',
        'id_sucursal__nombre'
    )
    date_hierarchy = 'fecha'
    inlines = [DetalleFacturaInline]
    list_per_page = 20

    def nombre_cliente(self, obj):
        return obj.id_cliente.persona.nombre_completo if obj.id_cliente and obj.id_cliente.persona else ''
    nombre_cliente.short_description = 'Cliente'

    def nombre_empleado(self, obj):
        return obj.id_empleado.persona.nombre_completo if obj.id_empleado and obj.id_empleado.persona else ''
    nombre_empleado.short_description = 'Empleado'

    def nombre_sucursal(self, obj):
        return obj.id_sucursal.nombre if obj.id_sucursal else ''
    nombre_sucursal.short_description = 'Sucursal'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editando un objeto existente
            return ['id_cliente', 'id_empleado', 'id_sucursal', 'fecha', 'total']
        return []


@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo DetalleFactura
    """
    list_display = (
        'id_detalle_factura',
        'id_factura',
        'id_producto',
        'cantidad',
        'precio_unitario',
        'subtotal'
    )
    list_filter = ('id_factura', 'id_producto')
    search_fields = (
        'id_factura__id_factura',
        'id_producto__nombre'
    )
    list_per_page = 20

    def has_add_permission(self, request):
        # Prevenir agregar detalles directamente, deben agregarse a través de Factura
        return False
