from django.contrib import admin
from .models import Producto, Categoria, Marca


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Categoria
    """
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Marca
    """
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Producto
    """
    list_display = ('id', 'nombre', 'precio', 'categoria', 'marca', 'estado')
    list_filter = ('categoria', 'marca', 'estado')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'estado')
    
    def categoria(self, obj):
        return obj.categoria.nombre
    categoria.short_description = 'Categoría'
    
    def marca(self, obj):
        return obj.marca.nombre
    marca.short_description = 'Marca'
