from django.contrib import admin
from .models import Inventario


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    """
    Admin configuration for Inventario model
    """
    list_display = ('id', 'producto', 'sucursal', 'cantidad', 'estado')
    list_filter = ('estado', 'sucursal', 'producto')
    search_fields = ('producto__nombre', 'sucursal__nombre')
    list_per_page = 20
    
    def get_queryset(self, request):
        """
        Optimize database queries by selecting related objects
        """
        return super().get_queryset(request).select_related('producto', 'sucursal')
