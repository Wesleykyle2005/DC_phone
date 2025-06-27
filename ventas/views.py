from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import requests
import os
from datetime import datetime

# Configuración de la API
API_BASE_URL = 'https://dc-phone-api.onrender.com/api'

def get_api_data(endpoint, params=None):
    """Función helper para obtener datos de la API"""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}", params=params)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error obteniendo datos de {endpoint}: {e}")
        return []

def post_api_data(endpoint, data):
    """Función helper para enviar datos a la API"""
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data)
        return response.status_code in (200, 201, 204)
    except Exception as e:
        print(f"Error enviando datos a {endpoint}: {e}")
        return False

def delete_api_data(endpoint):
    """Función helper para eliminar datos de la API"""
    try:
        response = requests.delete(f"{API_BASE_URL}/{endpoint}")
        return response.status_code == 200 or response.status_code == 204
    except Exception as e:
        print(f"Error eliminando datos de {endpoint}: {e}")
        return False

# Vistas para Facturas
class FacturaListView(View):
    template_name = 'ventas/factura_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        # Obtener facturas de la API
        facturas = get_api_data('Factura')
        # Obtener catálogos para mapear nombres
        clientes = get_api_data('Cliente')
        empleados = get_api_data('Empleado')
        sucursales = get_api_data('Sucursal')
        productos = get_api_data('Producto')
        inventarios = get_api_data('Inventario')
        # Crear diccionarios para acceso rápido
        clientes_dict = {c['idCliente']: c for c in clientes}
        empleados_dict = {e['idEmpleado']: e for e in empleados}
        sucursales_dict = {s['idSucursal']: s for s in sucursales}
        productos_dict = {p['idProducto']: p for p in productos}
        # Enriquecer facturas con nombres
        for factura in facturas:
            # Cliente
            id_cliente = factura.get('idCliente')
            cliente = clientes_dict.get(id_cliente)
            factura['nombreCliente'] = cliente['persona']['nombreCompletoPersona'] if cliente and cliente.get('persona') else 'Sin datos'
            # Empleado
            id_empleado = factura.get('idEmpleado')
            empleado = empleados_dict.get(id_empleado)
            factura['nombreEmpleado'] = empleado['persona']['nombreCompletoPersona'] if empleado and empleado.get('persona') else 'Sin datos'
            # Sucursal
            id_sucursal = factura.get('idSucursal')
            sucursal = sucursales_dict.get(id_sucursal)
            factura['nombreSucursal'] = sucursal['nombreSucursal'] if sucursal else 'Sin datos'
            # Enriquecer detalles con nombre de producto
            for detalle in factura.get('detallesFactura', []):
                id_producto = detalle.get('idProducto')
                producto = productos_dict.get(id_producto)
                detalle['nombreProducto'] = producto['nombreProducto'] if producto else 'Producto no encontrado'
        
        # Aplicar filtros de búsqueda
        search = request.GET.get('search', '')
        search_type = request.GET.get('search_type', 'cliente')
        
        if search:
            # Filtrar facturas según el tipo de búsqueda
            filtered_facturas = []
            for factura in facturas:
                if factura.get('estadoFactura', True):  # Solo facturas activas
                    if search_type == 'cliente' and factura.get('cliente'):
                        if search.lower() in factura['cliente'].get('persona', {}).get('nombreCompletoPersona', '').lower():
                            filtered_facturas.append(factura)
                    elif search_type == 'empleado' and factura.get('empleado'):
                        if search.lower() in factura['empleado'].get('persona', {}).get('nombreCompletoPersona', '').lower():
                            filtered_facturas.append(factura)
                    elif search_type == 'sucursal' and factura.get('sucursal'):
                        if search.lower() in factura['sucursal'].get('nombreSucursal', '').lower():
                            filtered_facturas.append(factura)
            facturas = filtered_facturas
        else:
            # Solo mostrar facturas activas
            facturas = [f for f in facturas if f.get('estadoFactura', True)]
        
        # Obtener datos para el formulario de nueva factura
        clientes = get_api_data('Cliente')
        empleados = get_api_data('Empleado')
        sucursales = get_api_data('Sucursal')
        productos = get_api_data('Producto')
        inventarios = get_api_data('Inventario')
        
        # Filtrar solo elementos activos
        clientes = [c for c in clientes if c.get('estadoCliente', True)]
        empleados = [e for e in empleados if e.get('estadoEmpleado', True)]
        sucursales = [s for s in sucursales if s.get('estadoSucursal', True)]
        productos = [p for p in productos if p.get('estadoProducto', True)]
        inventarios = [i for i in inventarios if i.get('estadoInventario', True)]
        
        # Preparar datos de productos por sucursal para el JavaScript
        productos_data = []
        for inventario in inventarios:
            producto = next((p for p in productos if p.get('idProducto') == inventario.get('idProducto')), None)
            sucursal = next((s for s in sucursales if s.get('idSucursal') == inventario.get('idSucursal')), None)
            if producto is not None and sucursal is not None and inventario.get('cantidadInventario', 0) > 0:
                productos_data.append({
                    'id': producto.get('idProducto'),
                    'nombre': producto.get('nombreProducto'),
                    'precio': float(producto.get('precioProducto', 0)),
                    'max_cantidad': inventario.get('cantidadInventario', 0),
                    'sucursal_id': sucursal.get('idSucursal')
                })
        
        # Obtener todos los detalles de factura
        detalles_api = get_api_data('DetalleFactura')
        detalles_por_factura = {}
        for detalle in detalles_api:
            id_factura = detalle.get('idFactura')
            if isinstance(id_factura, dict):
                id_factura = id_factura.get('idFactura')
            if id_factura:
                detalles_por_factura.setdefault(id_factura, []).append(detalle)

        # Enriquecer facturas con nombre de persona y detalles
        for factura in facturas:
            # Cliente
            cliente = factura.get('cliente')
            if cliente and not cliente.get('persona') and cliente.get('idPersona'):
                persona = get_api_data(f'Persona/{cliente.get("idPersona")}')
                if persona:
                    cliente['persona'] = persona
            # Empleado
            empleado = factura.get('empleado')
            if empleado and not empleado.get('persona') and empleado.get('idPersona'):
                persona = get_api_data(f'Persona/{empleado.get("idPersona")}')
                if persona:
                    empleado['persona'] = persona
            # Detalles de factura
            factura['detallesFactura'] = detalles_por_factura.get(factura.get('idFactura'), [])
        
        context = {
            'facturas': facturas,
            'clientes': clientes,
            'empleados': empleados,
            'sucursales': sucursales,
            'productos_data': productos_data,
        }
        
        return render(request, self.template_name, context)

class FacturaCreateView(View):
    template_name = 'ventas/factura_form.html'
    success_url = reverse_lazy('ventas:factura-list')

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        # Obtener datos para el formulario
        clientes = get_api_data('Cliente')
        empleados = get_api_data('Empleado')
        sucursales = get_api_data('Sucursal')
        productos = get_api_data('Producto')
        inventarios = get_api_data('Inventario')
        
        # Filtrar solo elementos activos
        clientes = [c for c in clientes if c.get('estadoCliente', True)]
        empleados = [e for e in empleados if e.get('estadoEmpleado', True)]
        sucursales = [s for s in sucursales if s.get('estadoSucursal', True)]
        productos = [p for p in productos if p.get('estadoProducto', True)]
        inventarios = [i for i in inventarios if i.get('estadoInventario', True)]
        
        # Preparar datos de productos por sucursal
        productos_data = []
        for inventario in inventarios:
            producto = next((p for p in productos if p.get('idProducto') == inventario.get('idProducto')), None)
            sucursal = next((s for s in sucursales if s.get('idSucursal') == inventario.get('idSucursal')), None)
            if producto is not None and sucursal is not None:
                productos_data.append({
                    'id': producto.get('idProducto'),
                    'nombre': producto.get('nombreProducto'),
                    'precio': float(producto.get('precioProducto', 0)),
                    'max_cantidad': inventario.get('cantidadInventario', 0),
                    'sucursal_id': sucursal.get('idSucursal')
                })
        
        context = {
            'clientes': clientes,
            'empleados': empleados,
            'sucursales': sucursales,
            'productos_data': productos_data,
        }
        
        return render(request, self.template_name, context)

    def post(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            # Obtener datos del formulario
            id_cliente = request.POST.get('id_cliente')
            id_empleado = request.POST.get('id_empleado')
            id_sucursal = request.POST.get('id_sucursal')
            total = request.POST.get('total', '0')
            # Obtener productos del formulario
            productos = request.POST.getlist('producto[]')
            cantidades = request.POST.getlist('cantidad[]')
            precios = request.POST.getlist('precio[]')
            subtotales = request.POST.getlist('subtotal[]')
            if not productos or not id_cliente or not id_empleado or not id_sucursal:
                messages.error(request, 'Todos los campos son obligatorios.')
                return redirect('ventas:factura-create')
            # Crear la factura
            factura_data = {
                'idCliente': int(id_cliente),
                'idEmpleado': int(id_empleado),
                'idSucursal': int(id_sucursal),
                'fechaFactura': datetime.now().isoformat(),
                'totalFactura': float(total),
                'estadoFactura': True
            }
            # Enviar factura a la API
            factura_response = requests.post(f"{API_BASE_URL}/Factura", json=factura_data, timeout=60)
            if factura_response.status_code in (200, 201):
                messages.success(request, 'Factura creada exitosamente.')
                # Obtener el ID de la factura creada de la respuesta
                factura_creada = factura_response.json()
                factura_id = factura_creada.get('idFactura')
                if factura_id:
                    # Crear detalles de factura
                    for i, producto_id in enumerate(productos):
                        if producto_id and cantidades[i] and precios[i]:
                            detalle_data = {
                                'idFactura': factura_id,
                                'idProducto': int(producto_id),
                                'cantidadDetalle': int(cantidades[i]),
                                'precioUnitarioDetalle': float(precios[i]),
                                'subtotalDetalle': float(subtotales[i])
                            }
                            post_api_data('DetalleFactura', detalle_data)
                return redirect(self.success_url)
            else:
                messages.error(request, f'Error al crear la factura: {factura_response.status_code}')
                return redirect('ventas:factura-create')
        except Exception as e:
            print(f"Error en creación de factura: {e}")
            messages.error(request, 'Error interno del servidor.')
            return redirect('ventas:factura-create')

class FacturaDetailView(View):
    template_name = 'ventas/factura_detail.html'

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        # Obtener factura específica de la API
        factura = get_api_data(f'Factura/{pk}')
        if not factura:
            messages.error(request, 'Factura no encontrada.')
            return redirect('ventas:factura-list')
        # Obtener catálogos
        clientes = get_api_data('Cliente')
        empleados = get_api_data('Empleado')
        sucursales = get_api_data('Sucursal')
        productos = get_api_data('Producto')
        # Diccionarios para acceso rápido
        clientes_dict = {c['idCliente']: c for c in clientes}
        empleados_dict = {e['idEmpleado']: e for e in empleados}
        sucursales_dict = {s['idSucursal']: s for s in sucursales}
        productos_dict = {p['idProducto']: p for p in productos}
        # Enriquecer factura
        id_cliente = factura.get('idCliente')
        cliente = clientes_dict.get(id_cliente)
        factura['nombreCliente'] = cliente['persona']['nombreCompletoPersona'] if cliente and cliente.get('persona') else 'Sin datos'
        id_empleado = factura.get('idEmpleado')
        empleado = empleados_dict.get(id_empleado)
        factura['nombreEmpleado'] = empleado['persona']['nombreCompletoPersona'] if empleado and empleado.get('persona') else 'Sin datos'
        id_sucursal = factura.get('idSucursal')
        sucursal = sucursales_dict.get(id_sucursal)
        factura['nombreSucursal'] = sucursal['nombreSucursal'] if sucursal else 'Sin datos'
        # Enriquecer detalles
        detalles_factura = factura.get('detallesFactura', [])
        for detalle in detalles_factura:
            id_producto = detalle.get('idProducto')
            producto = productos_dict.get(id_producto)
            detalle['nombreProducto'] = producto['nombreProducto'] if producto else 'Producto no encontrado'
        context = {
            'factura': factura,
            'detalles': detalles_factura,
        }
        return render(request, self.template_name, context)

class FacturaDeleteView(View):
    template_name = 'ventas/factura_confirm_delete.html'
    success_url = reverse_lazy('ventas:factura-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        # Obtener factura para mostrar información
        factura = get_api_data(f'Factura/{pk}')
        
        if not factura:
            messages.error(request, 'Factura no encontrada.')
            return redirect('ventas:factura-list')
        
        context = {'factura': factura}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        # Eliminar factura de la API
        if delete_api_data(f'Factura/{pk}'):
            messages.success(request, 'Factura eliminada exitosamente.')
        else:
            messages.error(request, 'Error al eliminar la factura.')
        
        return redirect(self.success_url)

class FacturaPDFView(View):
    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        # Obtener factura de la API
        factura = get_api_data(f'Factura/{pk}')
        if not factura:
            messages.error(request, 'Factura no encontrada.')
            return redirect('ventas:factura-list')
        # Obtener catálogos
        clientes = get_api_data('Cliente')
        empleados = get_api_data('Empleado')
        sucursales = get_api_data('Sucursal')
        productos = get_api_data('Producto')
        # Diccionarios para acceso rápido
        clientes_dict = {c['idCliente']: c for c in clientes}
        empleados_dict = {e['idEmpleado']: e for e in empleados}
        sucursales_dict = {s['idSucursal']: s for s in sucursales}
        productos_dict = {p['idProducto']: p for p in productos}
        # Enriquecer factura
        id_cliente = factura.get('idCliente')
        cliente = clientes_dict.get(id_cliente)
        factura['nombreCliente'] = cliente['persona']['nombreCompletoPersona'] if cliente and cliente.get('persona') else 'Sin datos'
        id_empleado = factura.get('idEmpleado')
        empleado = empleados_dict.get(id_empleado)
        factura['nombreEmpleado'] = empleado['persona']['nombreCompletoPersona'] if empleado and empleado.get('persona') else 'Sin datos'
        id_sucursal = factura.get('idSucursal')
        sucursal = sucursales_dict.get(id_sucursal)
        factura['nombreSucursal'] = sucursal['nombreSucursal'] if sucursal else 'Sin datos'
        # Obtener detalles de la API y enriquecer
        detalles_api = get_api_data('DetalleFactura')
        detalles_factura = [d for d in detalles_api if (d.get('idFactura') == pk or (isinstance(d.get('idFactura'), dict) and d.get('idFactura', {}).get('idFactura') == pk))]
        for detalle in detalles_factura:
            id_producto = detalle.get('idProducto')
            producto = productos_dict.get(id_producto)
            detalle['nombreProducto'] = producto['nombreProducto'] if producto else 'Producto no encontrado'
        
        # Crear respuesta PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="factura_{factura.get("idFactura")}.pdf"'
        
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # Logo alineado a la derecha, arriba
        logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'DC_phone.png')
        logo_width = 100
        logo_height = 60
        x_logo = width - logo_width - 60
        y_logo = height - 30 - logo_height
        
        try:
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA")
                p.drawImage(ImageReader(img), x_logo, y_logo, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Error al insertar el logo: {e}")

        # Encabezado
        p.setFont('Courier-Bold', 18)
        p.drawString((width - p.stringWidth('DC_phone', 'Courier-Bold', 18)) / 2, height - 60, "DC_phone")
        p.setFont('Courier', 10)
        p.drawString((width - p.stringWidth('Factura Electrónica', 'Courier', 10)) / 2, height - 80, "Factura Electrónica")
        
        # Información de la factura
        fecha_factura = datetime.fromisoformat(factura.get('fechaFactura', '').replace('Z', '+00:00'))
        p.drawString(40, height - 110, f"Fecha: {fecha_factura.strftime('%d/%m/%Y %H:%M')}")
        p.drawString(40, height - 125, f"Factura N°: {factura.get('idFactura')}")
        
        # Información del cliente
        p.drawString(40, height - 150, f"Cliente: {factura.get('nombreCliente', 'Sin datos')}")
        
        # Información del empleado
        p.drawString(40, height - 165, f"Empleado: {factura.get('nombreEmpleado', 'Sin datos')}")
        
        # Información de la sucursal
        p.drawString(40, height - 180, f"Sucursal: {factura.get('nombreSucursal', 'Sin datos')}")

        # Tabla de productos
        p.setFont('Courier-Bold', 12)
        p.drawString(40, height - 210, "Producto")
        p.drawString(250, height - 210, "Cantidad")
        p.drawString(320, height - 210, "Precio Unitario")
        p.drawString(430, height - 210, "Subtotal")
        p.line(40, height - 215, 540, height - 215)
        
        p.setFont('Courier', 10)
        y = height - 230
        
        for detalle in detalles_factura:
            nombre_producto = detalle.get('nombreProducto', 'Producto no encontrado')
            cantidad = detalle.get('cantidadDetalle', 0)
            precio_unitario = detalle.get('precioUnitarioDetalle', 0)
            subtotal = detalle.get('subtotalDetalle', 0)
            p.drawString(40, y, nombre_producto)
            p.drawString(250, y, str(cantidad))
            p.drawString(320, y, f"${precio_unitario:.2f}")
            p.drawString(430, y, f"${subtotal:.2f}")
            p.line(40, y - 3, 540, y - 3)
            y -= 18

        # Total
        p.setFont('Courier-Bold', 12)
        p.drawString(320, y - 10, "Total:")
        p.drawString(430, y - 10, f"${factura.get('totalFactura', 0):.2f}")

        p.showPage()
        p.save()
        
        return response
