"""
Standalone script to generate sample data for the phone_store project.
Run with: python generate_data.py
"""

import os
import sys
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Set up Django environment
import django

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phone_store.settings')
django.setup()

# Now import your models after Django is configured
from core.models import Municipio, Rol
from personas.models import Persona, Cliente, Empleado
from sucursales.models import Sucursal
from productos.models import Categoria, Marca, Producto
from inventario.models import Inventario
from ventas.models import Factura, DetalleFactura
from django.contrib.auth import get_user_model

class DataGenerator:
    def __init__(self):
        self.Usuario = get_user_model()
    
    def clear_data(self):
        """Clear existing data in reverse order of dependencies"""
        print("Clearing existing data...")
        
        # Primero eliminar el superusuario admin
        self.Usuario.objects.filter(username='admin').delete()
        
        # Luego eliminar datos que dependen de otros
        DetalleFactura.objects.all().delete()
        Factura.objects.all().delete()
        self.Usuario.objects.filter(is_superuser=False).delete()
        Inventario.objects.all().delete()
        Producto.objects.all().delete()
        Categoria.objects.all().delete()
        Marca.objects.all().delete()
        Empleado.objects.all().delete()
        Cliente.objects.all().delete()
        Persona.objects.all().delete()
        Sucursal.objects.all().delete()
        
        # Finalmente eliminar datos base
        Rol.objects.all().delete()
        Municipio.objects.all().delete()
    
    def load_core_data(self):
        """Load core data (municipios and roles)"""
        print("Loading core data...")
        
        # Municipios
        municipios = [
            {'codigo_municipio': 'MUN001', 'nombre_municipio': 'San Salvador'},
            {'codigo_municipio': 'MUN002', 'nombre_municipio': 'Santa Tecla'},
            {'codigo_municipio': 'MUN003', 'nombre_municipio': 'Soyapango'},
            {'codigo_municipio': 'MUN004', 'nombre_municipio': 'San Miguel'},
            {'codigo_municipio': 'MUN005', 'nombre_municipio': 'Santa Ana'},
        ]
        for m in municipios:
            Municipio.objects.get_or_create(**m)
        
        # Roles
        roles = [
            {'nombre_rol': 'Administrador'},
            {'nombre_rol': 'Vendedor'},
            {'nombre_rol': 'Bodeguero'},
            {'nombre_rol': 'Gerente'},
        ]
        for r in roles:
            Rol.objects.get_or_create(**r)
    
    def load_sucursales(self):
        """Load sucursales"""
        print("Loading sucursales...")
        
        sucursales = [
            {
                'nombre': 'Sucursal Centro',
                'direccion': 'Calle Principal #123',
                'telefono': '2222-0000',
                'municipio': 'MUN001'
            },
            {
                'nombre': 'Sucursal Norte',
                'direccion': 'Avenida Norte #456',
                'telefono': '2222-1111',
                'municipio': 'MUN002'
            },
            {
                'nombre': 'Sucursal Sur',
                'direccion': 'Boulevard del Sur #789',
                'telefono': '2222-2222',
                'municipio': 'MUN003'
            }
        ]
        
        for s in sucursales:
            municipio = Municipio.objects.get(codigo_municipio=s.pop('municipio'))
            Sucursal.objects.get_or_create(
                municipio=municipio,
                defaults=s
            )
    
    def load_personas(self):
        """Load sample personas"""
        print("Loading personas...")
        
        nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Sofía', 'Pedro', 'Laura']
        apellidos = ['Pérez', 'González', 'Martínez', 'López', 'Rodríguez', 'Hernández', 'García']
        
        for i in range(1, 51):  # 50 personas
            Persona.objects.get_or_create(
                dni=f'0000000{i:02d}-{random.randint(0,9)}',
                defaults={
                    'nombre_completo': f'{random.choice(nombres)} {random.choice(apellidos)}',
                    'telefono': f'7{random.randint(1000000, 9999999)}',
                    'codigo_municipio': Municipio.objects.order_by('?').first(),
                    'estado': True
                }
            )
    
    def load_empleados_clientes(self):
        """Load empleados and clientes"""
        print("Loading empleados and clientes...")
        
        # First 30 personas are clientes
        for persona in Persona.objects.all()[:30]:
            Cliente.objects.get_or_create(persona=persona)
        
        # Next 20 personas are empleados
        for persona in Persona.objects.all()[30:50]:
            Empleado.objects.get_or_create(
                persona=persona,
                defaults={
                    'id_sucursal': Sucursal.objects.order_by('?').first(),
                    'direccion': f'Calle {random.randint(1, 100)} # {random.randint(1, 100)}'
                }
            )
    
    def load_productos(self):
        """Load categorias, marcas and productos"""
        print("Loading productos...")
        
        # Categorias
        categorias = [
            {'nombre': 'Smartphones'},
            {'nombre': 'Tablets'},
            {'nombre': 'Accesorios'},
        ]
        for c in categorias:
            Categoria.objects.get_or_create(**c)
        
        # Marcas
        marcas = [
            {'nombre': 'Samsung'},
            {'nombre': 'Apple'},
            {'nombre': 'Xiaomi'},
            {'nombre': 'Huawei'},
        ]
        for m in marcas:
            Marca.objects.get_or_create(**m)
        
        # Productos
        productos = [
            # Smartphones
            ('Galaxy S21', 'Smartphone gama alta', 999.99, 'Smartphones', 'Samsung'),
            ('iPhone 13', 'Último modelo de Apple', 1199.99, 'Smartphones', 'Apple'),
            ('Redmi Note 10', 'Excelente relación calidad-precio', 299.99, 'Smartphones', 'Xiaomi'),
            
            # Tablets
            ('Galaxy Tab S7', 'Tablet de alta gama', 649.99, 'Tablets', 'Samsung'),
            ('iPad Air', 'Tablet versátil', 599.99, 'Tablets', 'Apple'),
            
            # Accesorios
            ('Funda protectora', 'Protege tu dispositivo', 19.99, 'Accesorios', 'Samsung'),
            ('Vidrio templado', 'Protección de pantalla', 9.99, 'Accesorios', 'Apple'),
        ]
        
        for nombre, desc, precio, cat_nombre, marca_nombre in productos:
            Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': desc,
                    'precio': Decimal(str(precio)),
                    'categoria': Categoria.objects.get(nombre=cat_nombre),
                    'marca': Marca.objects.get(nombre=marca_nombre),
                    'estado': True
                }
            )
    
    def load_inventario(self):
        """Load inventory data"""
        print("Loading inventario...")
        
        for producto in Producto.objects.all():
            for sucursal in Sucursal.objects.all():
                Inventario.objects.get_or_create(
                    producto=producto,
                    sucursal=sucursal,
                    defaults={'cantidad': random.randint(0, 50)}
                )
    
    def load_usuarios(self):
        """Load users"""
        print("Loading usuarios...")
        
        # Create admin user
        if not self.Usuario.objects.filter(username='admin').exists():
            self.Usuario.objects.create_superuser(
                username='admin',
                email='admin@phonestore.com',
                password='admin123',
                id_rol=Rol.objects.get(nombre_rol='Administrador'),
                estado=True
            )
        
        # Create employee users
        for i, empleado in enumerate(Empleado.objects.all(), 1):
            username = f'empleado{i}'
            if not self.Usuario.objects.filter(username=username).exists():
                self.Usuario.objects.create_user(
                    username=username,
                    email=f'{username}@phonestore.com',
                    password='empleado123',
                    id_empleado=empleado,
                    id_rol=Rol.objects.exclude(nombre_rol='Administrador').order_by('?').first(),
                    is_staff=True,
                    estado=True
                )
    
    def load_ventas(self):
        """Load sales data"""
        print("Loading ventas...")
        
        # Create 100 facturas
        for i in range(100):
            factura = Factura.objects.create(
                id_cliente=Cliente.objects.order_by('?').first(),
                id_empleado=Empleado.objects.order_by('?').first(),
                id_sucursal=Sucursal.objects.order_by('?').first(),
                fecha=datetime.now() - timedelta(days=random.randint(0, 90)),
                total=Decimal('0.00'),
                estado=random.choice([True, True, True, False])
            )
            
            # Add 1-5 items per factura
            total = Decimal('0.00')
            for _ in range(random.randint(1, 5)):
                producto = Producto.objects.order_by('?').first()
                cantidad = random.randint(1, 3)
                precio_unitario = producto.precio
                subtotal = precio_unitario * cantidad
                total += subtotal
                
                DetalleFactura.objects.create(
                    id_factura=factura,
                    id_producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal
                )
            
            factura.total = total
            factura.save()
    
    def run(self):
        """Run the data generation process"""
        try:
            self.clear_data()
            self.load_core_data()
            self.load_sucursales()
            self.load_personas()
            self.load_empleados_clientes()
            self.load_productos()
            self.load_inventario()
            self.load_usuarios()
            self.load_ventas()
            print("\n¡Datos de muestra generados exitosamente!")
            print("Usuario administrador:")
            print("  Usuario: admin")
            print("  Contraseña: admin123")
            print("\nUsuarios de empleados:")
            print("  Usuario: empleado1, empleado2, etc.")
            print("  Contraseña: empleado123")
        except Exception as e:
            print(f"\nError generando datos: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("Iniciando generación de datos de muestra...")
    generator = DataGenerator()
    generator.run()
