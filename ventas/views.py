from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.db.models import Q
from .models import Factura, DetalleFactura
from personas.models import Cliente, Empleado
from sucursales.models import Sucursal
from productos.models import Producto
from inventario.models import Inventario
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.conf import settings
import os
from reportlab.lib.utils import ImageReader
from PIL import Image

# Create your views here.

# Vistas para Facturas
class FacturaListView(LoginRequiredMixin, ListView):
    model = Factura
    template_name = 'ventas/factura_list.html'
    context_object_name = 'facturas'
    paginate_by = 10

    def get_queryset(self):
        queryset = Factura.objects.filter(estado=True).order_by('-fecha')
        search_query = self.request.GET.get('search', '')
        search_type = self.request.GET.get('search_type', 'cliente')
        if search_query:
            if search_type == 'cliente':
                queryset = queryset.filter(
                    Q(id_cliente__persona__nombre_completo__icontains=search_query)
                )
            elif search_type == 'empleado':
                queryset = queryset.filter(
                    Q(id_empleado__persona__nombre_completo__icontains=search_query)
                )
            elif search_type == 'sucursal':
                queryset = queryset.filter(
                    Q(id_sucursal__nombre__icontains=search_query)
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.all()
        context['empleados'] = Empleado.objects.all()
        context['sucursales'] = Sucursal.objects.all()
        # Productos activos y sus cantidades máximas por inventario
        productos = Producto.objects.filter(estado=True)
        inventario = Inventario.objects.filter(estado=True)
        productos_data = []
        for inv in inventario:
            if inv.cantidad > 0:
                productos_data.append({
                    'id': inv.producto.id,
                    'nombre': inv.producto.nombre,
                    'precio': float(inv.producto.precio),
                    'max_cantidad': inv.cantidad,
                    'sucursal_id': inv.sucursal.id
                })
        context['productos_data'] = productos_data
        return context

class FacturaCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        clientes = Cliente.objects.all()
        empleados = Empleado.objects.all()
        sucursales = Sucursal.objects.all()
        productos = Producto.objects.filter(estado=True)
        inventario = Inventario.objects.filter(estado=True)
        productos_data = []
        for inv in inventario:
            if inv.cantidad > 0:
                productos_data.append({
                    'id': inv.producto.id,
                    'nombre': inv.producto.nombre,
                    'precio': float(inv.producto.precio),
                    'max_cantidad': inv.cantidad,
                    'sucursal_id': inv.sucursal.id
                })
        return render(request, 'ventas/factura_list.html', {
            'clientes': clientes,
            'empleados': empleados,
            'sucursales': sucursales,
            'productos_data': productos_data,
        })

    def post(self, request, *args, **kwargs):
        id_cliente = request.POST.get('id_cliente')
        id_empleado = request.POST.get('id_empleado')
        id_sucursal = request.POST.get('id_sucursal')
        productos = request.POST.getlist('producto[]')
        cantidades = request.POST.getlist('cantidad[]')
        if not (id_cliente and id_empleado and id_sucursal and productos and cantidades and len(productos) == len(cantidades)):
            messages.error(request, 'Todos los campos son obligatorios y debe seleccionar al menos un producto.')
            return redirect('ventas:factura-list')
        # Crear factura (total se calcula después)
        factura = Factura.objects.create(
            id_cliente_id=id_cliente,
            id_empleado_id=id_empleado,
            id_sucursal_id=id_sucursal,
            total=0,
            estado=True
        )
        total = 0
        for prod_id, cant in zip(productos, cantidades):
            if not prod_id or not cant:
                continue
            producto = Producto.objects.get(pk=prod_id)
            precio = producto.precio
            subtotal = int(cant) * float(precio)
            DetalleFactura.objects.create(
                id_factura=factura,
                id_producto=producto,
                cantidad=cant,
                precio_unitario=precio,
                subtotal=subtotal
            )
            total += subtotal
        factura.total = total
        factura.save()
        messages.success(request, f'Factura #{factura.id_factura} creada exitosamente.')
        return redirect('ventas:factura-list')

class FacturaDeleteView(LoginRequiredMixin, DeleteView):
    model = Factura
    success_url = reverse_lazy('ventas:factura-list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = False
        self.object.save()
        messages.success(request, f'Factura #{self.object.id_factura} desactivada exitosamente.')
        return HttpResponseRedirect(self.get_success_url())

class FacturaPDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        factura = Factura.objects.select_related('id_cliente__persona', 'id_empleado__persona', 'id_sucursal').get(pk=pk)
        detalles = DetalleFactura.objects.filter(id_factura=factura)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="factura_{factura.id_factura}.pdf"'
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # Logo alineado a la derecha, arriba
        logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'DC_phone.png')
        logo_width = 100
        logo_height = 60
        x_logo = width - logo_width - 60  # margen derecho de 60
        y_logo = height - 30 - logo_height  # margen superior de 60
        try:
            print(f"[PDF] Intentando cargar logo en: {logo_path}")
            if not os.path.exists(logo_path):
                print(f"[PDF] Archivo no encontrado: {logo_path}")
            else:
                print(f"[PDF] Archivo encontrado. Intentando abrir con PIL...")
                img = Image.open(logo_path)
                print(f"[PDF] Imagen abierta. Modo: {img.mode}, Tamaño: {img.size}")
                if img.mode not in ("RGB", "RGBA"):
                    print(f"[PDF] Convirtiendo imagen a RGBA...")
                    img = img.convert("RGBA")
                print(f"[PDF] Insertando imagen en x={x_logo}, y={y_logo}, w={logo_width}, h={logo_height}")
                p.drawImage(ImageReader(img), x_logo, y_logo, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')
                print(f"[PDF] Imagen insertada correctamente.")
        except Exception as e:
            print(f"[PDF] Error al insertar el logo: {e}")

        # Cambiar tipografía a Courier para estilo de factura antigua
        p.setFont('Courier-Bold', 18)
        p.drawString((width - p.stringWidth('DC_phone', 'Courier-Bold', 18)) / 2, height - 60, "DC_phone")
        p.setFont('Courier', 10)
        p.drawString((width - p.stringWidth('Factura Electrónica', 'Courier', 10)) / 2, height - 80, "Factura Electrónica")
        p.setFont('Courier', 10)
        p.drawString(40, height - 110, f"Fecha: {factura.fecha.strftime('%d/%m/%Y %H:%M')}")
        p.drawString(40, height - 125, f"Factura N°: {factura.id_factura}")
        p.drawString(40, height - 150, f"Cliente: {factura.id_cliente.persona.nombre_completo}")
        p.drawString(40, height - 165, f"Empleado: {factura.id_empleado.persona.nombre_completo}")
        p.drawString(40, height - 180, f"Sucursal: {factura.id_sucursal.nombre}")

        # Tabla de productos
        p.setFont('Courier-Bold', 12)
        p.drawString(40, height - 210, "Producto")
        p.drawString(250, height - 210, "Cantidad")
        p.drawString(320, height - 210, "Precio Unitario")
        p.drawString(430, height - 210, "Subtotal")
        p.line(40, height - 215, 540, height - 215)
        p.setFont('Courier', 10)
        y = height - 230
        for detalle in detalles:
            p.drawString(40, y, detalle.id_producto.nombre)
            p.drawString(250, y, str(detalle.cantidad))
            p.drawString(320, y, f"${detalle.precio_unitario:.2f}")
            p.drawString(430, y, f"${detalle.subtotal:.2f}")
            p.line(40, y - 3, 540, y - 3)
            y -= 18

        # Total
        p.setFont('Courier-Bold', 12)
        p.drawString(320, y - 10, "Total:")
        p.drawString(430, y - 10, f"${factura.total:.2f}")

        p.showPage()

        p.save()
        return response
