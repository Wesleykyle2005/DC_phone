from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
import requests

# Create your views here.

# Vistas para Sucursales
class SucursalListView(View):
    template_name = 'sucursales/sucursal_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        url = "https://dc-phone-api.onrender.com/api/Sucursal"
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                sucursales_api = response.json()
                sucursales = []
                for s in sucursales_api:
                    if s.get('estadoSucursal', True):
                        municipio_data = s.get('municipio')
                        if municipio_data is None:
                            municipio = {'nombre_municipio': 'Indefinido', 'codigo_municipio': ''}
                        else:
                            municipio = {
                                'nombre_municipio': municipio_data.get('nombreMunicipio', 'N/A'),
                                'codigo_municipio': municipio_data.get('idMunicipio', '')
                            }
                        sucursal = {
                            'id': s.get('idSucursal'),
                            'nombre': s.get('nombreSucursal'),
                            'direccion': s.get('direccionSucursal'),
                            'telefono': s.get('telefonoSucursal'),
                            'estado': s.get('estadoSucursal'),
                            'municipio': municipio
                        }
                        sucursales.append(sucursal)
                # Búsqueda
                search_query = request.GET.get('search', '')
                if search_query:
                    sucursales = [
                        s for s in sucursales
                        if (search_query.lower() in s.get('nombre', '').lower() or
                            search_query.lower() in s.get('direccion', '').lower() or
                            search_query.lower() in s.get('telefono', '').lower() or
                            search_query.lower() in s.get('municipio', {}).get('nombre_municipio', '').lower())
                    ]
                # Cargar municipios para el modal
                municipios = []
                try:
                    municipios_response = requests.get("https://dc-phone-api.onrender.com/api/Municipio", timeout=60)
                    if municipios_response.status_code == 200:
                        municipios_api = municipios_response.json()
                        municipios = [
                            {
                                'codigo_municipio': m.get('idMunicipio'),
                                'nombre_municipio': m.get('nombreMunicipio')
                            }
                            for m in municipios_api if m.get('estadoMunicipio', True)
                        ]
                except Exception as e:
                    print(f"Error cargando municipios: {e}")
                return render(request, self.template_name, {
                    'sucursales': sucursales,
                    'search_query': search_query,
                    'municipios': municipios
                })
            else:
                messages.error(request, f'Error al cargar sucursales: {response.status_code}')
                return render(request, self.template_name, {
                    'sucursales': [],
                    'municipios': []
                })
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
            return render(request, self.template_name, {
                'sucursales': [],
                'municipios': []
            })
        except Exception as e:
            messages.error(request, f'Error de conexión: {str(e)}')
            return render(request, self.template_name, {
                'sucursales': [],
                'municipios': []
            })

class SucursalCreateView(View):
    success_url = reverse_lazy('sucursales:sucursal-list')

    def post(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        try:
            nombre = request.POST.get('nombre')
            direccion = request.POST.get('direccion')
            telefono = request.POST.get('telefono')
            municipio_id = request.POST.get('municipio')
            if not all([nombre, direccion, municipio_id]):
                messages.error(request, 'Todos los campos obligatorios deben ser completados.')
                return redirect('sucursales:sucursal-list')
            url = "https://dc-phone-api.onrender.com/api/Sucursal"
            payload = {
                "nombreSucursal": nombre,
                "direccionSucursal": direccion,
                "telefonoSucursal": telefono or "",
                "idMunicipio": municipio_id,
                "estadoSucursal": True
            }
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code in (200, 201, 204):
                messages.success(request, f'Sucursal "{nombre}" creada exitosamente.')
            else:
                messages.error(request, f'Error al crear sucursal: {response.status_code}')
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except Exception as e:
            messages.error(request, f'Error al crear sucursal: {str(e)}')
        return redirect(self.success_url)

class SucursalDeleteView(View):
    success_url = reverse_lazy('sucursales:sucursal-list')

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        try:
            url = f"https://dc-phone-api.onrender.com/api/Sucursal/{pk}"
            response = requests.delete(url, timeout=60)
            if response.status_code == 200:
                messages.success(request, 'Sucursal eliminada exitosamente.')
            else:
                messages.error(request, f'Error al eliminar sucursal: {response.status_code}')
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except Exception as e:
            messages.error(request, f'Error al eliminar sucursal: {str(e)}')
        return redirect(self.success_url)

class SucursalGraficasView(View):
    template_name = 'sucursales/sucursal_graficas.html'

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        try:
            # 1. Obtener información de la sucursal
            url = f"https://dc-phone-api.onrender.com/api/Sucursal/{pk}"
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                sucursal_data = response.json()
                sucursal = {
                    'id': sucursal_data.get('idSucursal'),
                    'nombre': sucursal_data.get('nombreSucursal'),
                    'direccion': sucursal_data.get('direccionSucursal'),
                    'telefono': sucursal_data.get('telefonoSucursal'),
                    'municipio': (sucursal_data.get('municipio') or {}).get('nombreMunicipio', 'Indefinido')
                }
                # 2. Obtener todas las facturas
                facturas_response = requests.get("https://dc-phone-api.onrender.com/api/Factura", timeout=60)
                facturas = []
                if facturas_response.status_code == 200:
                    facturas_api = facturas_response.json()
                    # Filtrar facturas de esta sucursal y activas
                    facturas = [f for f in facturas_api if str(f.get('idSucursal')) == str(pk) and f.get('estadoFactura', True)]
                # 3. Obtener todos los detalles de factura
                detalles_response = requests.get("https://dc-phone-api.onrender.com/api/DetalleFactura", timeout=60)
                detalles = []
                if detalles_response.status_code == 200:
                    detalles_api = detalles_response.json()
                    factura_ids = [f.get('idFactura') for f in facturas]
                    detalles = [d for d in detalles_api if (d.get('idFactura') in factura_ids or (isinstance(d.get('idFactura'), dict) and d.get('idFactura', {}).get('idFactura') in factura_ids))]
                # 4. Obtener inventario de la sucursal
                inventario_response = requests.get("https://dc-phone-api.onrender.com/api/Inventario", timeout=60)
                inventario = []
                if inventario_response.status_code == 200:
                    inventario_api = inventario_response.json()
                    inventario = [i for i in inventario_api if str(i.get('idSucursal')) == str(pk) and i.get('estadoInventario', True)]
                # 5. Obtener productos
                productos_response = requests.get("https://dc-phone-api.onrender.com/api/Producto", timeout=60)
                productos = {}
                if productos_response.status_code == 200:
                    productos_api = productos_response.json()
                    productos = {p.get('idProducto'): p for p in productos_api if p.get('estadoProducto', True)}
                # 6. Obtener empleados
                empleados_response = requests.get("https://dc-phone-api.onrender.com/api/Empleado", timeout=60)
                empleados = {}
                if empleados_response.status_code == 200:
                    empleados_api = empleados_response.json()
                    empleados = {e.get('idEmpleado'): e for e in empleados_api if e.get('estadoEmpleado', True)}
                # 7. Procesar datos para métricas
                from datetime import datetime, timedelta
                from collections import defaultdict
                import calendar
                # Ventas por mes (ya existente)
                ventas_mensuales = defaultdict(float)
                meses_nombres = list(calendar.month_name)[1:]
                # Ventas por día (nuevo)
                ventas_diarias = defaultdict(float)
                for factura in facturas:
                    fecha_str = factura.get('fechaFactura', '')
                    if fecha_str:
                        try:
                            fecha = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
                            if fecha >= datetime.now() - timedelta(days=365):
                                mes_key = f"{fecha.year}-{fecha.month:02d}"
                                ventas_mensuales[mes_key] += float(factura.get('totalFactura', 0))
                                dia_key = fecha.strftime('%d/%m/%Y')
                                ventas_diarias[dia_key] += float(factura.get('totalFactura', 0))
                        except Exception:
                            continue
                ventas_mensuales_ordenadas = []
                for mes_key in sorted(ventas_mensuales.keys()):
                    year, month = mes_key.split('-')
                    ventas_mensuales_ordenadas.append({
                        'mes': f"{meses_nombres[int(month)-1]} {year}",
                        'total': ventas_mensuales[mes_key]
                    })
                ventas_diarias_ordenadas = []
                for dia_key in sorted(ventas_diarias.keys(), key=lambda x: datetime.strptime(x, '%d/%m/%Y')):
                    ventas_diarias_ordenadas.append({
                        'dia': dia_key,
                        'total': ventas_diarias[dia_key]
                    })
                # Productos más vendidos
                productos_vendidos = defaultdict(lambda: {'cantidad': 0, 'total': 0, 'producto': None})
                for detalle in detalles:
                    id_producto = detalle.get('idProducto')
                    if isinstance(id_producto, dict):
                        id_producto = id_producto.get('idProducto')
                    if id_producto in productos:
                        producto = productos[id_producto]
                        cantidad = detalle.get('cantidadDetalle', 0)
                        subtotal = float(detalle.get('subtotalDetalle', 0))
                        productos_vendidos[id_producto]['cantidad'] += cantidad
                        productos_vendidos[id_producto]['total'] += subtotal
                        productos_vendidos[id_producto]['producto'] = producto
                productos_mas_vendidos = []
                for id_producto, datos in sorted(productos_vendidos.items(), key=lambda x: x[1]['cantidad'], reverse=True)[:10]:
                    producto = datos['producto']
                    productos_mas_vendidos.append({
                        'producto': producto.get('nombreProducto', 'Producto Desconocido') if producto else 'Producto Desconocido',
                        'cantidad': datos['cantidad'],
                        'total': datos['total'],
                        'marca': (producto.get('marca', {}) or {}).get('nombreMarca', 'Sin marca') if producto else 'Sin marca'
                    })
                # Inventario actual
                inventario_actual = []
                for inv in inventario:
                    id_producto = inv.get('idProducto')
                    if id_producto in productos:
                        producto = productos[id_producto]
                        inventario_actual.append({
                            'producto': producto.get('nombreProducto', 'Producto Desconocido') if producto else 'Producto Desconocido',
                            'stock': inv.get('cantidadInventario', 0),
                            'marca': (producto.get('marca', {}) or {}).get('nombreMarca', 'Sin marca') if producto else 'Sin marca',
                            'categoria': (producto.get('categoria', {}) or {}).get('nombreCategoria', 'Sin categoría') if producto else 'Sin categoría'
                        })
                inventario_actual.sort(key=lambda x: x['stock'])
                # Rendimiento de empleados
                rendimiento_empleados = defaultdict(lambda: {'ventas': 0, 'facturas': 0, 'empleado': None})
                for factura in facturas:
                    id_empleado = factura.get('idEmpleado')
                    if isinstance(id_empleado, dict):
                        id_empleado = id_empleado.get('idEmpleado')
                    if id_empleado in empleados:
                        empleado = empleados[id_empleado]
                        total = float(factura.get('totalFactura', 0))
                        rendimiento_empleados[id_empleado]['ventas'] += total
                        rendimiento_empleados[id_empleado]['facturas'] += 1
                        rendimiento_empleados[id_empleado]['empleado'] = empleado
                rendimiento_empleados_lista = []
                for id_empleado, datos in sorted(rendimiento_empleados.items(), key=lambda x: x[1]['ventas'], reverse=True):
                    empleado = datos['empleado']
                    persona = (empleado.get('persona', {}) or {}) if empleado else {}
                    rendimiento_empleados_lista.append({
                        'empleado': persona.get('nombreCompletoPersona', 'Empleado Desconocido'),
                        'ventas': datos['ventas'],
                        'facturas': datos['facturas'],
                        'promedio': datos['ventas'] / datos['facturas'] if datos['facturas'] > 0 else 0
                    })
                context = {
                    'sucursal': sucursal,
                    'ventas_mensuales': ventas_mensuales_ordenadas,
                    'ventas_diarias': ventas_diarias_ordenadas,
                    'productos_mas_vendidos': productos_mas_vendidos,
                    'inventario_actual': inventario_actual,
                    'rendimiento_empleados': rendimiento_empleados_lista,
                }
                return render(request, self.template_name, context)
            else:
                messages.error(request, f'Error al cargar la sucursal: {response.status_code}')
                return redirect('sucursales:sucursal-list')
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
            return redirect('sucursales:sucursal-list')
        except Exception as e:
            messages.error(request, f'Error al cargar la sucursal: {str(e)}')
            return redirect('sucursales:sucursal-list')

class SucursalUpdateView(View):
    success_url = reverse_lazy('sucursales:sucursal-list')

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            # Obtener datos del formulario
            nombre = request.POST.get('nombre')
            direccion = request.POST.get('direccion')
            telefono = request.POST.get('telefono')
            municipio_id = request.POST.get('municipio')
            
            # Validar datos
            if not all([nombre, direccion, municipio_id]):
                messages.error(request, 'Todos los campos obligatorios deben ser completados.')
                return redirect('sucursales:sucursal-list')
            
            # Actualizar sucursal vía API
            url = f"https://dc-phone-api.onrender.com/api/Sucursal/{pk}"
            payload = {
                "idSucursal": pk,
                "nombreSucursal": nombre,
                "direccionSucursal": direccion,
                "telefonoSucursal": telefono or "",
                "idMunicipio": municipio_id,
                "estadoSucursal": True
            }
            
            response = requests.put(url, json=payload, timeout=60)
            if response.status_code in (200, 201, 204):
                messages.success(request, f'Sucursal "{nombre}" actualizada exitosamente.')
            else:
                messages.error(request, f'Error al actualizar sucursal: {response.status_code}')
                
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except Exception as e:
            messages.error(request, f'Error al actualizar sucursal: {str(e)}')
        
        return redirect(self.success_url)
