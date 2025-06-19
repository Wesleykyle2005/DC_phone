from django.urls import path
from . import views

app_name = 'sucursales'

urlpatterns = [
    # URLs para Sucursales
    path('', views.SucursalListView.as_view(), name='sucursal-list'),
    path('crear/', views.SucursalCreateView.as_view(), name='sucursal-create'),
    path('<int:pk>/delete/', views.SucursalDeleteView.as_view(), name='sucursal-delete'),
] 