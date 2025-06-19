from django.urls import path
from . import views

app_name = 'personas'

urlpatterns = [
    # URLs para Clientes
    path('clientes/', views.ClienteListView.as_view(), name='cliente-list'),
    path('clientes/crear/', views.ClienteCreateView.as_view(), name='cliente-create'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente-update'),
    path('clientes/<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente-delete'),
    
    # URLs para Empleados
    path('empleados/', views.EmpleadoListView.as_view(), name='empleado-list'),
    path('empleados/crear/', views.EmpleadoCreateView.as_view(), name='empleado-create'),
    path('empleados/<int:pk>/editar/', views.EmpleadoUpdateView.as_view(), name='empleado-update'),
    path('empleados/<int:pk>/eliminar/', views.EmpleadoDeleteView.as_view(), name='empleado-delete'),
] 