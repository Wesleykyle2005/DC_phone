from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    # URLs para Municipios
    path('municipios/', views.MunicipioListView.as_view(), name='municipio-list'),
    path('municipios/crear/', views.MunicipioCreateView.as_view(), name='municipio-create'),
    path('municipios/<int:pk>/editar/', views.MunicipioUpdateView.as_view(), name='municipio-update'),
    path('municipios/<int:pk>/eliminar/', views.MunicipioDeleteView.as_view(), name='municipio-delete'),
    
    # URLs para Roles
    path('roles/', views.RolListView.as_view(), name='rol-list'),
    path('roles/crear/', views.RolCreateView.as_view(), name='rol-create'),
    path('roles/<int:pk>/editar/', views.RolUpdateView.as_view(), name='rol-update'),
    path('roles/<int:pk>/eliminar/', views.RolDeleteView.as_view(), name='rol-delete'),

    path('otros/', views.OtrosListCreateView.as_view(), name='otros-list'),
]
