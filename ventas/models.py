# ventas/models.py
from django.db import models
from personas.models import Cliente, Empleado
from sucursales.models import Sucursal
from productos.models import Producto

class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)

class DetalleFactura(models.Model):
    id_detalle_factura = models.AutoField(primary_key=True)
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)