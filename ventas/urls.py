from django.urls import path
from . import views
from .views import FacturaPDFView, FacturaExportExcelView

app_name = 'ventas'

urlpatterns = [
    # URLs para Facturas
    path('', views.FacturaListView.as_view(), name='factura-list'),
    path('crear/', views.FacturaCreateView.as_view(), name='factura-create'),
    path('<int:pk>/', views.FacturaDetailView.as_view(), name='factura-detail'),
    path('<int:pk>/delete/', views.FacturaDeleteView.as_view(), name='factura-delete'),
    path('<int:pk>/imprimir/', FacturaPDFView.as_view(), name='factura-imprimir'),
    path('exportar_excel/', FacturaExportExcelView.as_view(), name='factura-export-excel'),
] 