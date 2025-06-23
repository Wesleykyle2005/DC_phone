from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
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
class FacturaListView(View):
    template_name = 'ventas/factura_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        # Aquí deberías consumir la API para obtener facturas
        facturas = []
        return render(request, self.template_name, {'facturas': facturas})

class FacturaCreateView(View):
    template_name = 'ventas/factura_form.html'
    success_url = reverse_lazy('ventas:factura-list')

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request):
        # Aquí deberías consumir la API para crear factura
        return redirect(self.success_url)

class FacturaDetailView(View):
    template_name = 'ventas/factura_detail.html'

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        # Aquí deberías consumir la API para obtener la factura
        factura = {}
        return render(request, self.template_name, {'factura': factura})

class FacturaDeleteView(View):
    template_name = 'ventas/factura_confirm_delete.html'
    success_url = reverse_lazy('ventas:factura-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request, pk):
        # Aquí deberías consumir la API para eliminar factura
        return redirect(self.success_url)

class FacturaPDFView(View):
    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
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
