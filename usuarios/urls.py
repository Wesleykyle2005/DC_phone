from django.urls import path, include
from . import views
from core.views import CustomLoginView

app_name = 'usuarios'

urlpatterns = [
    # URLs para Usuarios
    path('', views.PersonaListCreateView.as_view(), name='persona-list'),
    path('crear/', views.UsuarioCreateView.as_view(), name='usuario-create'),
    path('<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario-update'),
    path('<int:pk>/eliminar/', views.UsuarioDeleteView.as_view(), name='usuario-delete'),
    
    # URLs de Autenticación
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
] 