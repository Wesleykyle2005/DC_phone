from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # URLs para Inventario
    path('', views.InventarioListView.as_view(), name='inventario-list'),
    path('crear/', views.InventarioCreateView.as_view(), name='inventario-create'),
    path('<int:pk>/delete/', views.InventarioDeleteView.as_view(), name='inventario-delete'),
    path('<int:pk>/update/', views.InventarioUpdateView.as_view(), name='inventario-update'),
] 