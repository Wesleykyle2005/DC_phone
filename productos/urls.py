from django.urls import path
from . import views

app_name = 'productos'
 
urlpatterns = [
    path('', views.ProductoListView.as_view(), name='producto-list'),
    path('crear/', views.ProductoCreateView.as_view(), name='producto-create'),
    path('<int:pk>/delete/', views.ProductoDeleteView.as_view(), name='producto-delete'),
] 