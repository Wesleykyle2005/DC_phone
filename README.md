# 📱 Phone Store - Sistema de Gestión de Tienda de Teléfonos

## Descripción General

**Phone Store** es un sistema integral de gestión para una tienda de teléfonos, desarrollado en Django. Permite administrar productos, inventario, sucursales, ventas (facturación), usuarios, roles, clientes, empleados y catálogos auxiliares. El sistema está diseñado para ofrecer una experiencia moderna, robusta y profesional, con autenticación, navegación intuitiva, generación de facturas en PDF y validaciones tanto en frontend como backend.

---

## Estructura del Proyecto

- **core/**: Catálogos auxiliares (municipios, roles) y vistas generales.
- **personas/**: Gestión de personas, clientes y empleados.
- **productos/**: Administración de productos, marcas y categorías.
- **sucursales/**: Gestión de sucursales físicas.
- **inventario/**: Control de inventario por sucursal y producto.
- **usuarios/**: Gestión de usuarios del sistema y autenticación.
- **ventas/**: Facturación, detalles de venta y generación de PDFs.
- **static/** y **templates/**: Archivos estáticos y plantillas base/globales.

---

## Funcionalidades Principales

- **CRUD completo** para productos, inventario, sucursales, personas, usuarios y catálogos.
- **Autenticación**: Login, logout, protección de vistas y control de acceso.
- **Facturación**: Creación de facturas, selección dinámica de productos, control de stock, generación de PDF con logo y formato profesional.
- **Catálogos auxiliares**: Gestión de municipios, roles, marcas y categorías desde una vista unificada.
- **Paginación, búsqueda y filtrado** en todas las vistas principales.
- **Validaciones**: Frontend (JS) y backend (Django), con mensajes claros y modales de confirmación.
- **Experiencia de usuario moderna**: Bootstrap, navegación centralizada, modales, feedback visual.

---

## Bibliotecas y Dependencias

- **Django**: Framework principal.
- **Pillow**: Manipulación de imágenes (para el logo en PDF).
- **ReportLab**: Generación de PDFs para facturas.
- **Bootstrap**: (vía CDN en templates) para el diseño responsivo.
- **Otros**: Bibliotecas estándar de Python y Django (os, datetime, etc.).

> **Nota:** Si no tienes un `requirements.txt`, puedes instalar lo esencial con:
> ```
> pip install django pillow reportlab
> ```

---

## Estructura de Modelos

### core/models.py

| Modelo     | Campos                                                                 |
|------------|------------------------------------------------------------------------|
| Municipio  | codigo_municipio (PK), nombre_municipio                                |
| Rol        | id_rol (PK), nombre_rol                                                |

---

### personas/models.py

| Modelo   | Campos                                                                                       |
|----------|----------------------------------------------------------------------------------------------|
| Persona  | id_persona (PK), dni, nombre_completo, telefono, codigo_municipio (FK), estado               |
| Cliente  | id_cliente (PK), persona (OneToOne FK)                                                       |
| Empleado | id_empleado (PK), persona (OneToOne FK), direccion, id_sucursal (FK a Sucursal)              |

---

### productos/models.py

| Modelo    | Campos                                                                                      |
|-----------|---------------------------------------------------------------------------------------------|
| Categoria | nombre                                                                                      |
| Marca     | nombre                                                                                      |
| Producto  | nombre, descripcion, precio, categoria (FK), marca (FK), estado                             |

---

### sucursales/models.py

| Modelo    | Campos                                                                                      |
|-----------|---------------------------------------------------------------------------------------------|
| Sucursal  | nombre, direccion, telefono, municipio (FK), estado                                         |

---

### inventario/models.py

| Modelo     | Campos                                                                                     |
|------------|--------------------------------------------------------------------------------------------|
| Inventario | producto (FK), sucursal (FK), cantidad, estado                                             |

---

### usuarios/models.py

| Modelo   | Campos                                                                                       |
|----------|----------------------------------------------------------------------------------------------|
| Usuario  | (hereda de AbstractUser), id_empleado (OneToOne FK), id_rol (FK), estado                     |

---

### ventas/models.py

| Modelo         | Campos                                                                                 |
|----------------|----------------------------------------------------------------------------------------|
| Factura        | id_factura (PK), id_cliente (FK), id_empleado (FK), id_sucursal (FK), fecha, total, estado |
| DetalleFactura | id_detalle_factura (PK), id_factura (FK), id_producto (FK), cantidad, precio_unitario, subtotal |

---

## Descripción de cada módulo/app

### core
- Catálogos auxiliares: municipios y roles.
- Vista de bienvenida y login centralizado.
- Gestión unificada de catálogos (municipios, roles, marcas, categorías).

### personas
- Gestión de personas, clientes y empleados.
- Asignación de empleados a sucursales.
- Filtros y búsquedas por tipo.

### productos
- CRUD de productos, marcas y categorías.
- Filtros por estado, búsqueda y paginación.

### sucursales
- Administración de sucursales físicas.
- Relación con municipios y empleados.

### inventario
- Control de stock por producto y sucursal.
- Solo productos y sucursales activos.

### usuarios
- Gestión de usuarios del sistema (hereda de AbstractUser).
- Asignación de roles y empleados.
- Autenticación y control de acceso.

### ventas
- Gestión de facturas y detalles de venta.
- Selección dinámica de productos según inventario.
- Generación de PDF profesional con logo y tipografía tipo factura antigua.

---

## Instalación y Ejecución

1. Instala dependencias:
   ```
   pip install django pillow reportlab
   ```
2. Realiza migraciones:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Crea un superusuario:
   ```
   python manage.py createsuperuser
   ```
4. Ejecuta el servidor:
   ```
   python manage.py runserver
   ```

---

## Créditos

Desarrollado por Wesley y colaboradores.  
¡Disfruta gestionando tu tienda de teléfonos con eficiencia y estilo! 