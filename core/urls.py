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

    # URLs para Marcas
    path('marcas/', views.MarcaListView.as_view(), name='marca-list'),
    path('marcas/crear/', views.MarcaCreateView.as_view(), name='marca-create'),
    path('marcas/<int:pk>/editar/', views.MarcaUpdateView.as_view(), name='marca-update'),
    path('marcas/<int:pk>/eliminar/', views.MarcaDeleteView.as_view(), name='marca-delete'),
    
    # URLs para Categorías
    path('categorias/', views.CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/crear/', views.CategoriaCreateView.as_view(), name='categoria-create'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaDeleteView.as_view(), name='categoria-delete'),

    path('otros/', views.OtrosListCreateView.as_view(), name='otros-list'),
]
