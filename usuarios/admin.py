from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .models import Usuario  # Comentado porque el modelo Usuario ya no existe


# @admin.register(Usuario)
# class UsuarioAdmin(UserAdmin):
#     """
#     Admin configuration for the custom Usuario model
#     """
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'estado')
#     list_filter = ('is_staff', 'is_superuser', 'estado', 'id_rol')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     ordering = ('username',)
#     filter_horizontal = ('groups', 'user_permissions')
#     list_per_page = 20
#     
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
#         ('Permissions', {
#             'fields': ('is_active', 'estado', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#         ('Custom fields', {'fields': ('id_empleado', 'id_rol')}),
#     )
