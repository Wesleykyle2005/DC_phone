from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
import requests
from ventas.export_excel import export_to_excel
from django.http import HttpResponse

# Create your views here.

# Vistas para Inventario
class InventarioListView(View):
    template_name = 'inventario/inventario_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        url = "https://dc-phone-api.onrender.com/api/Inventario"
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                inventarios_api = response.json()
                inventarios = []
                for inv in inventarios_api:
                    if inv.get('estadoInventario', True):
                        sucursal_data = inv.get('sucursal')
                        if sucursal_data is None:
                            sucursal = {'id': None, 'nombre': 'Indefinido'}
                        else:
                            sucursal = {
                                'id': sucursal_data.get('idSucursal'),
                                'nombre': sucursal_data.get('nombreSucursal', 'N/A')
                            }
                        producto_data = inv.get('producto')
                        if producto_data is None:
                            producto = {'id': None, 'nombre': 'Indefinido'}
                        else:
                            producto = {
                                'id': producto_data.get('idProducto'),
                                'nombre': producto_data.get('nombreProducto', 'N/A')
                            }
                        inventario = {
                            'id': inv.get('idInventario'),
                            'cantidad': inv.get('cantidadInventario'),
                            'estado': inv.get('estadoInventario'),
                            'producto': producto,
                            'sucursal': sucursal
                        }
                        inventarios.append(inventario)
                # Búsqueda
                search_query = request.GET.get('search', '')
                if search_query:
                    inventarios = [
                        i for i in inventarios
                        if (search_query.lower() in i.get('producto', {}).get('nombre', '').lower() or
                            search_query.lower() in i.get('sucursal', {}).get('nombre', '').lower())
                    ]
                # Cargar productos y sucursales activos para el modal
                productos = []
                sucursales = []
                try:
                    productos_response = requests.get("https://dc-phone-api.onrender.com/api/Producto", timeout=60)
                    sucursales_response = requests.get("https://dc-phone-api.onrender.com/api/Sucursal", timeout=60)
                    if productos_response.status_code == 200:
                        productos_api = productos_response.json()
                        productos = [
                            {'id': p.get('idProducto'), 'nombre': p.get('nombreProducto')}
                            for p in productos_api if p.get('estadoProducto', True)
                        ]
                    if sucursales_response.status_code == 200:
                        sucursales_api = sucursales_response.json()
                        sucursales = [
                            {'id': s.get('idSucursal'), 'nombre': s.get('nombreSucursal')}
                            for s in sucursales_api if s.get('estadoSucursal', True)
                        ]
                except Exception as e:
                    print(f"Error cargando productos/sucursales: {e}")
                return render(request, self.template_name, {
                    'inventarios': inventarios,
                    'search_query': search_query,
                    'productos': productos,
                    'sucursales': sucursales
                })
            else:
                messages.error(request, f'Error al cargar inventario: {response.status_code}')
                return render(request, self.template_name, {
                    'inventarios': [],
                    'productos': [],
                    'sucursales': []
                })
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
            return render(request, self.template_name, {
                'inventarios': [],
                'productos': [],
                'sucursales': []
            })
        except Exception as e:
            messages.error(request, f'Error de conexión: {str(e)}')
            return render(request, self.template_name, {
                'inventarios': [],
                'productos': [],
                'sucursales': []
            })

class InventarioCreateView(View):
    success_url = reverse_lazy('inventario:inventario-list')

    def post(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        try:
            producto_id = request.POST.get('producto')
            sucursal_id = request.POST.get('sucursal')
            cantidad = request.POST.get('cantidad')
            if not all([producto_id, sucursal_id, cantidad]):
                messages.error(request, 'Todos los campos obligatorios deben ser completados.')
                return redirect('inventario:inventario-list')
            url = "https://dc-phone-api.onrender.com/api/Inventario"
            payload = {
                "idProducto": int(producto_id),
                "idSucursal": int(sucursal_id),
                "cantidadInventario": int(cantidad),
                "estadoInventario": True
            }
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code in (200, 201, 204):
                messages.success(request, 'Inventario creado exitosamente.')
            else:
                messages.error(request, f'Error al crear inventario: {response.status_code}')
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except ValueError:
            messages.error(request, 'Error: La cantidad debe ser un número válido.')
        except Exception as e:
            messages.error(request, f'Error al crear inventario: {str(e)}')
        return redirect(self.success_url)

class InventarioDeleteView(View):
    success_url = reverse_lazy('inventario:inventario-list')

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        try:
            url = f"https://dc-phone-api.onrender.com/api/Inventario/{pk}"
            response = requests.delete(url, timeout=60)
            if response.status_code == 200:
                messages.success(request, 'Inventario eliminado exitosamente.')
            else:
                messages.error(request, f'Error al eliminar inventario: {response.status_code}')
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except Exception as e:
            messages.error(request, f'Error al eliminar inventario: {str(e)}')
        return redirect(self.success_url)

class InventarioUpdateView(View):
    success_url = reverse_lazy('inventario:inventario-list')

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            # Obtener datos del formulario
            producto_id = request.POST.get('producto')
            sucursal_id = request.POST.get('sucursal')
            cantidad = request.POST.get('cantidad')
            
            # Validar datos
            if not all([producto_id, sucursal_id, cantidad]):
                messages.error(request, 'Todos los campos obligatorios deben ser completados.')
                return redirect('inventario:inventario-list')
            
            # Actualizar inventario vía API
            url = f"https://dc-phone-api.onrender.com/api/Inventario/{pk}"
            payload = {
                "idInventario": pk,
                "idProducto": int(producto_id),
                "idSucursal": int(sucursal_id),
                "cantidadInventario": int(cantidad),
                "estadoInventario": True
            }
            
            response = requests.put(url, json=payload, timeout=60)
            if response.status_code in (200, 201, 204):
                messages.success(request, 'Inventario actualizado exitosamente.')
            else:
                messages.error(request, f'Error al actualizar inventario: {response.status_code}')
                
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except ValueError:
            messages.error(request, 'Error: La cantidad debe ser un número válido.')
        except Exception as e:
            messages.error(request, f'Error al actualizar inventario: {str(e)}')
        
        return redirect(self.success_url)

class InventarioExportExcelView(View):
    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        url = "https://dc-phone-api.onrender.com/api/Inventario"
        response = requests.get(url, timeout=60)
        inventarios_api = response.json() if response.status_code == 200 else []
        inventarios = []
        for inv in inventarios_api:
            if inv.get('estadoInventario', True):
                sucursal_data = inv.get('sucursal')
                if sucursal_data is None:
                    sucursal = 'Indefinido'
                else:
                    sucursal = sucursal_data.get('nombreSucursal', 'N/A')
                producto_data = inv.get('producto')
                if producto_data is None:
                    producto = 'Indefinido'
                else:
                    producto = producto_data.get('nombreProducto', 'N/A')
                inventario = {
                    'producto': producto,
                    'sucursal': sucursal,
                    'cantidad': inv.get('cantidadInventario')
                }
                inventarios.append(inventario)
        columnas = [
            ("producto", "Producto"),
            ("sucursal", "Sucursal"),
            ("cantidad", "Cantidad")
        ]
        output = export_to_excel(inventarios, columnas, nombre_archivo="inventario.xlsx")
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=inventario.xlsx'
        return response
