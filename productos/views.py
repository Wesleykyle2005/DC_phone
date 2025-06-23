from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
import requests

# Create your views here.

# Vistas para Productos
class ProductoListView(View):
    template_name = 'productos/producto_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        # Consumir la API para obtener productos
        url = "https://dc-phone-api.onrender.com/api/Producto"
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                productos_api = response.json()
                
                # Mapear los datos de la API al formato que espera la plantilla
                productos = []
                for producto_api in productos_api:
                    if producto_api.get('estadoProducto', True):  # Solo productos activos
                        producto = {
                            'id': producto_api.get('idProducto'),
                            'nombre': producto_api.get('nombreProducto'),
                            'descripcion': producto_api.get('descripcionProducto'),
                            'precio': producto_api.get('precioProducto'),
                            'estado': producto_api.get('estadoProducto'),
                            'categoria': {
                                'nombre': producto_api.get('categoria', {}).get('nombreCategoria', 'N/A')
                            },
                            'marca': {
                                'nombre': producto_api.get('marca', {}).get('nombreMarca', 'N/A')
                            }
                        }
                        productos.append(producto)
                
                # Aplicar búsqueda si se proporciona
                search_query = request.GET.get('search', '')
                if search_query:
                    productos = [
                        p for p in productos 
                        if (search_query.lower() in p.get('nombre', '').lower() or
                            search_query.lower() in p.get('descripcion', '').lower() or
                            search_query.lower() in p.get('categoria', {}).get('nombre', '').lower() or
                            search_query.lower() in p.get('marca', {}).get('nombre', '').lower())
                    ]
                
                # Cargar categorías y marcas para el modal de creación
                categorias = []
                marcas = []
                try:
                    categorias_response = requests.get("https://dc-phone-api.onrender.com/api/Categoria", timeout=60)
                    marcas_response = requests.get("https://dc-phone-api.onrender.com/api/Marca", timeout=60)
                    
                    if categorias_response.status_code == 200:
                        categorias_api = categorias_response.json()
                        categorias = [{'id': c.get('idCategoria'), 'nombre': c.get('nombreCategoria')} 
                                    for c in categorias_api if c.get('estadoCategoria', True)]
                    
                    if marcas_response.status_code == 200:
                        marcas_api = marcas_response.json()
                        marcas = [{'id': m.get('idMarca'), 'nombre': m.get('nombreMarca')} 
                                for m in marcas_api if m.get('estadoMarca', True)]
                except Exception as e:
                    print(f"Error cargando categorías/marcas: {e}")
                
                return render(request, self.template_name, {
                    'productos': productos,
                    'search_query': search_query,
                    'categorias': categorias,
                    'marcas': marcas
                })
            else:
                messages.error(request, f'Error al cargar productos: {response.status_code}')
                return render(request, self.template_name, {
                    'productos': [],
                    'categorias': [],
                    'marcas': []
                })
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
            return render(request, self.template_name, {
                'productos': [],
                'categorias': [],
                'marcas': []
            })
        except Exception as e:
            messages.error(request, f'Error de conexión: {str(e)}')
            return render(request, self.template_name, {
                'productos': [],
                'categorias': [],
                'marcas': []
            })

class ProductoCreateView(View):
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('productos:producto-list')

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        # Cargar categorías y marcas para el formulario
        try:
            categorias_response = requests.get("https://dc-phone-api.onrender.com/api/Categoria", timeout=60)
            marcas_response = requests.get("https://dc-phone-api.onrender.com/api/Marca", timeout=60)
            
            categorias = []
            marcas = []
            
            if categorias_response.status_code == 200:
                categorias_api = categorias_response.json()
                categorias = [{'id': c.get('idCategoria'), 'nombre': c.get('nombreCategoria')} 
                            for c in categorias_api if c.get('estadoCategoria', True)]
            
            if marcas_response.status_code == 200:
                marcas_api = marcas_response.json()
                marcas = [{'id': m.get('idMarca'), 'nombre': m.get('nombreMarca')} 
                        for m in marcas_api if m.get('estadoMarca', True)]
            
            return render(request, self.template_name, {
                'categorias': categorias,
                'marcas': marcas
            })
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
            return render(request, self.template_name, {
                'categorias': [],
                'marcas': []
            })
        except Exception as e:
            messages.error(request, f'Error al cargar datos: {str(e)}')
            return render(request, self.template_name, {
                'categorias': [],
                'marcas': []
            })

    def post(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            # Obtener datos del formulario (usando los nombres del modal)
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            precio = request.POST.get('precio')
            categoria_id = request.POST.get('categoria')
            marca_id = request.POST.get('marca')
            
            # Validar datos
            if not all([nombre, precio, categoria_id, marca_id]):
                messages.error(request, 'Todos los campos obligatorios deben ser completados.')
                return redirect('productos:producto-list')
            
            # Crear producto vía API
            url = "https://dc-phone-api.onrender.com/api/Producto"
            payload = {
                "nombreProducto": nombre,
                "descripcionProducto": descripcion or "",
                "precioProducto": float(precio),
                "idCategoria": int(categoria_id),
                "idMarca": int(marca_id),
                "estadoProducto": True
            }
            
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code in (200, 201):
                messages.success(request, f'Producto "{nombre}" creado exitosamente.')
            else:
                messages.error(request, f'Error al crear producto: {response.status_code}')
                
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except ValueError:
            messages.error(request, 'Error: El precio debe ser un número válido.')
        except Exception as e:
            messages.error(request, f'Error al crear producto: {str(e)}')
        
        return redirect(self.success_url)

class ProductoDeleteView(View):
    success_url = reverse_lazy('productos:producto-list')

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            # Eliminar producto vía API
            url = f"https://dc-phone-api.onrender.com/api/Producto/{pk}"
            response = requests.delete(url, timeout=60)
            
            if response.status_code == 200:
                messages.success(request, 'Producto eliminado exitosamente.')
            else:
                messages.error(request, f'Error al eliminar producto: {response.status_code}')
                
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except Exception as e:
            messages.error(request, f'Error al eliminar producto: {str(e)}')
        
        return redirect(self.success_url)
