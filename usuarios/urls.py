from django.urls import path, include
from . import views
from core.views import CustomLoginView
from .views import ExportarClientesExcelView, ExportarEmpleadosExcelView

app_name = 'usuarios'

urlpatterns = [
    # URLs para Usuarios
    path('', views.PersonaListCreateView.as_view(), name='persona-list'),
    path('crear/', views.UsuarioCreateView.as_view(), name='usuario-create'),
    path('<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario-update'),
    path('<int:pk>/eliminar/', views.UsuarioDeleteView.as_view(), name='usuario-delete'),
    
    # URLs para Personas
    path('persona/<int:pk>/eliminar/', views.PersonaDeleteView.as_view(), name='persona-delete'),
    
    # URLs de Autenticación
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    path('personas/exportar_clientes_excel/', ExportarClientesExcelView.as_view(), name='exportar-clientes-excel'),
    path('personas/exportar_empleados_excel/', ExportarEmpleadosExcelView.as_view(), name='exportar-empleados-excel'),
] 