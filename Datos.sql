-- Script SQL para crear la base de datos de Phone Store (con ON DELETE SET NULL en todas las claves foráneas y campos foráneos NULL donde aplica)

-- Tabla: Municipio
CREATE TABLE Municipio (
    IdMunicipio VARCHAR(10) PRIMARY KEY,
    NombreMunicipio VARCHAR(50) NOT NULL
);

-- Tabla: Rol
CREATE TABLE Rol (
    IdRol INT IDENTITY(1,1) PRIMARY KEY,
    NombreRol VARCHAR(50) NOT NULL
);

-- Tabla: Categoria
CREATE TABLE Categoria (
    IdCategoria INT IDENTITY(1,1) PRIMARY KEY,
    NombreCategoria VARCHAR(50) NOT NULL
);

-- Tabla: Marca
CREATE TABLE Marca (
    IdMarca INT IDENTITY(1,1) PRIMARY KEY,
    NombreMarca VARCHAR(50) NOT NULL
);

-- Tabla: Producto
CREATE TABLE Producto (
    IdProducto INT IDENTITY(1,1) PRIMARY KEY,
    NombreProducto VARCHAR(100) NOT NULL,
    DescripcionProducto TEXT NULL,
    PrecioProducto DECIMAL(10,2) NOT NULL,
    IdCategoria INT NULL,
    IdMarca INT NULL,
    EstadoProducto BIT DEFAULT 1,
    CONSTRAINT CK_PrecioProducto_Positivo CHECK (PrecioProducto > 0),
    FOREIGN KEY (IdCategoria) REFERENCES Categoria(IdCategoria) ON DELETE SET NULL,
    FOREIGN KEY (IdMarca) REFERENCES Marca(IdMarca) ON DELETE SET NULL
);

-- Tabla: Sucursal
CREATE TABLE Sucursal (
    IdSucursal INT IDENTITY(1,1) PRIMARY KEY,
    NombreSucursal VARCHAR(50) NOT NULL,
    DireccionSucursal VARCHAR(200) NOT NULL,
    TelefonoSucursal VARCHAR(15) NULL,
    IdMunicipio VARCHAR(10) NULL,
    EstadoSucursal BIT DEFAULT 1,
    FOREIGN KEY (IdMunicipio) REFERENCES Municipio(IdMunicipio) ON DELETE SET NULL
);

-- Tabla: Persona
CREATE TABLE Persona (
    IdPersona INT IDENTITY(1,1) PRIMARY KEY,
    DniPersona VARCHAR(20) UNIQUE NOT NULL,
    NombreCompletoPersona VARCHAR(100) NOT NULL,
    TelefonoPersona VARCHAR(15) NULL,
    IdMunicipio VARCHAR(10) NULL,
    EstadoPersona BIT DEFAULT 1,
    FOREIGN KEY (IdMunicipio) REFERENCES Municipio(IdMunicipio) ON DELETE SET NULL
);

-- Tabla: Cliente
CREATE TABLE Cliente (
    IdCliente INT IDENTITY(1,1) PRIMARY KEY,
    IdPersona INT UNIQUE NULL,
    FOREIGN KEY (IdPersona) REFERENCES Persona(IdPersona) ON DELETE SET NULL
);

-- Tabla: Empleado
CREATE TABLE Empleado (
    IdEmpleado INT IDENTITY(1,1) PRIMARY KEY,
    IdPersona INT UNIQUE NULL,
    DireccionEmpleado VARCHAR(200) NOT NULL,
    IdSucursal INT NULL,
    FOREIGN KEY (IdPersona) REFERENCES Persona(IdPersona) ON DELETE SET NULL,
    FOREIGN KEY (IdSucursal) REFERENCES Sucursal(IdSucursal) ON DELETE SET NULL
);

-- Tabla: Usuario
CREATE TABLE Usuario (
    IdUsuario INT IDENTITY(1,1) PRIMARY KEY,
    ContrasenaUsuario VARCHAR(128) NOT NULL,
    UltimoInicioSesion DATETIME2 NULL,
    EsSuperUsuario BIT NOT NULL DEFAULT 0,
    NombreUsuario VARCHAR(150) UNIQUE NOT NULL,
    Nombre VARCHAR(150) NOT NULL,
    Apellido VARCHAR(150) NOT NULL,
    CorreoElectronico VARCHAR(254) NOT NULL,
    EsPersonal BIT NOT NULL DEFAULT 0,
    EsActivo BIT NOT NULL DEFAULT 1,
    FechaRegistro DATETIME2 NOT NULL DEFAULT GETDATE(),
    IdEmpleado INT NULL,
    IdRol INT NULL,
    EstadoUsuario BIT DEFAULT 1,
    FOREIGN KEY (IdEmpleado) REFERENCES Empleado(IdEmpleado) ON DELETE SET NULL,
    FOREIGN KEY (IdRol) REFERENCES Rol(IdRol) ON DELETE SET NULL
);

-- Tabla: Inventario
CREATE TABLE Inventario (
    IdInventario INT IDENTITY(1,1) PRIMARY KEY,
    IdProducto INT NULL,
    IdSucursal INT NULL,
    CantidadInventario INT NOT NULL,
    EstadoInventario BIT DEFAULT 1,
    CONSTRAINT CK_CantidadInventario_Positiva CHECK (CantidadInventario >= 0),
    FOREIGN KEY (IdProducto) REFERENCES Producto(IdProducto) ON DELETE SET NULL,
    FOREIGN KEY (IdSucursal) REFERENCES Sucursal(IdSucursal) ON DELETE SET NULL
);

-- Tabla: Factura
CREATE TABLE Factura (
    IdFactura INT IDENTITY(1,1) PRIMARY KEY,
    IdCliente INT NULL,
    IdEmpleado INT NULL,
    IdSucursal INT NULL,
    FechaFactura DATETIME2 NOT NULL DEFAULT GETDATE(),
    TotalFactura DECIMAL(10,2) NOT NULL,
    EstadoFactura BIT DEFAULT 1,
    FOREIGN KEY (IdCliente) REFERENCES Cliente(IdCliente) ON DELETE SET NULL,
    FOREIGN KEY (IdEmpleado) REFERENCES Empleado(IdEmpleado) ON DELETE SET NULL,
    FOREIGN KEY (IdSucursal) REFERENCES Sucursal(IdSucursal) ON DELETE SET NULL
);

-- Tabla: DetalleFactura
CREATE TABLE DetalleFactura (
    IdDetalleFactura INT IDENTITY(1,1) PRIMARY KEY,
    IdFactura INT NULL,
    IdProducto INT NULL,
    CantidadDetalle INT NOT NULL,
    PrecioUnitarioDetalle DECIMAL(10,2) NOT NULL,
    SubtotalDetalle DECIMAL(10,2) NOT NULL,
    CONSTRAINT CK_CantidadDetalle_Positiva CHECK (CantidadDetalle > 0),
    CONSTRAINT CK_PrecioUnitarioDetalle_Positivo CHECK (PrecioUnitarioDetalle > 0),
    FOREIGN KEY (IdFactura) REFERENCES Factura(IdFactura) ON DELETE SET NULL,
    FOREIGN KEY (IdProducto) REFERENCES Producto(IdProducto) ON DELETE SET NULL
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX IX_Producto_Categoria ON Producto(IdCategoria);
CREATE INDEX IX_Producto_Marca ON Producto(IdMarca);
CREATE INDEX IX_Sucursal_Municipio ON Sucursal(IdMunicipio);
CREATE INDEX IX_Persona_Municipio ON Persona(IdMunicipio);
CREATE INDEX IX_Empleado_Sucursal ON Empleado(IdSucursal);
CREATE INDEX IX_Inventario_Producto ON Inventario(IdProducto);
CREATE INDEX IX_Inventario_Sucursal ON Inventario(IdSucursal);
CREATE INDEX IX_Factura_Cliente ON Factura(IdCliente);
CREATE INDEX IX_Factura_Empleado ON Factura(IdEmpleado);
CREATE INDEX IX_Factura_Sucursal ON Factura(IdSucursal);
CREATE INDEX IX_DetalleFactura_Factura ON DetalleFactura(IdFactura);
CREATE INDEX IX_DetalleFactura_Producto ON DetalleFactura(IdProducto);



DROP TABLE Categoria
Go
DROP TABLE Cliente
Go
DROP TABLE DetalleFactura
Go
DROP TABLE Empleado
Go
DROP TABLE Factura
Go
DROP TABLE Inventario
Go
DROP TABLE Marca
Go
DROP TABLE Municipio
Go
DROP TABLE Persona
Go
DROP TABLE Producto
Go
DROP TABLE Rol
Go
DROP TABLE Sucursal
Go
DROP TABLE Usuario
Go

-- Script SQL para inserción de datos en la base de datos Phone Store
-- Orden lógico para respetar dependencias de claves foráneas
-- Datos adaptados al contexto de Nicaragua

-- 1. Inserción en Municipio
INSERT INTO Municipio (IdMunicipio, NombreMunicipio) VALUES
('01', 'Managua'),
('02', 'León'),
('03', 'Granada'),
('04', 'Masaya'),
('05', 'Estelí');

-- 2. Inserción en Rol
INSERT INTO Rol (NombreRol) VALUES
('Administrador'),
('Vendedor'),
('Gerente'),
('Soporte Técnico');

-- 3. Inserción en Categoria
INSERT INTO Categoria (NombreCategoria) VALUES
('Smartphones'),
('Accesorios'),
('Tablets'),
('Smartwatches');

-- 4. Inserción en Marca
INSERT INTO Marca (NombreMarca) VALUES
('Samsung'),
('Apple'),
('Xiaomi'),
('Huawei'),
('Motorola');

-- 5. Inserción en Producto
INSERT INTO Producto (NombreProducto, DescripcionProducto, PrecioProducto, IdCategoria, IdMarca, EstadoProducto) VALUES
('Samsung Galaxy A54', 'Smartphone con pantalla AMOLED 6.4", 128GB', 12500.00, 1, 1, 1),
('iPhone 14 Pro', 'Smartphone con chip A16 Bionic, 256GB', 35000.00, 1, 2, 1),
('Xiaomi Redmi Note 12', 'Smartphone con cámara 50MP, 64GB', 8000.00, 1, 3, 1),
('Huawei Watch GT 3', 'Smartwatch con monitoreo de salud', 6000.00, 4, 4, 1),
('Funda Samsung A54', 'Funda protectora de silicona', 300.00, 2, 1, 1),
('Motorola Edge 40', 'Smartphone 5G con 256GB', 18000.00, 1, 5, 1);

-- 6. Inserción en Sucursal
INSERT INTO Sucursal (NombreSucursal, DireccionSucursal, TelefonoSucursal, IdMunicipio, EstadoSucursal) VALUES
('Sucursal Metrocentro', 'Centro Comercial Metrocentro, Managua', '2255-1234', '01', 1),
('Sucursal León', 'Calle Central, León', '2311-5678', '02', 1),
('Sucursal Granada', 'Plaza Colonial, Granada', '2552-9012', '03', 1);

-- 7. Inserción en Persona
INSERT INTO Persona (DniPersona, NombreCompletoPersona, TelefonoPersona, IdMunicipio, EstadoPersona) VALUES
('001-010190-0001F', 'Juan José Pérez González', '8888-1234', '01', 1),
('002-150285-0002G', 'María Alejandra López Ramírez', '8765-4321', '02', 1),
('003-200395-0003H', 'Carlos Eduardo Gómez Martínez', '8456-7890', '01', 1),
('004-101188-0004J', 'Ana Sofía Morales Vargas', '8999-4567', '03', 1),
('005-050492-0005K', 'Luis Antonio Rivera Ortega', '8777-8901', '01', 1),
('006-251098-0006L', 'Claudia Isabel Castillo Flores', '8666-2345', '02', 1);

-- 8. Inserción en Cliente
INSERT INTO Cliente (IdPersona) VALUES
(1), -- Juan José Pérez
(4), -- Ana Sofía Morales
(6); -- Claudia Isabel Castillo

-- 9. Inserción en Empleado
INSERT INTO Empleado (IdPersona, DireccionEmpleado, IdSucursal) VALUES
(2, 'Barrio San José, León', 2), -- María Alejandra López
(3, 'Colonia Centroamérica, Managua', 1), -- Carlos Eduardo Gómez
(5, 'Reparto El Carmen, Managua', 1); -- Luis Antonio Rivera

-- 10. Inserción en Usuario
INSERT INTO Usuario (ContrasenaUsuario, UltimoInicioSesion, EsSuperUsuario, NombreUsuario, Nombre, Apellido, CorreoElectronico, EsPersonal, EsActivo, FechaRegistro, IdEmpleado, IdRol, EstadoUsuario) VALUES
('hashed_pass_admin', NULL, 1, 'admin1', 'Carlos', 'Gómez', 'carlos.gomez@phonestore.ni', 1, 1, '2025-06-01', 2, 1, 1), -- Admin (Carlos)
('hashed_pass_vendedor', NULL, 0, 'vendedor1', 'María', 'López', 'maria.lopez@phonestore.ni', 1, 1, '2025-06-02', 1, 2, 1), -- Vendedor (María)
('hashed_pass_gerente', NULL, 0, 'gerente1', 'Luis', 'Rivera', 'luis.rivera@phonestore.ni', 1, 1, '2025-06-03', 3, 3, 1); -- Gerente (Luis)

-- 11. Inserción en Inventario
INSERT INTO Inventario (IdProducto, IdSucursal, CantidadInventario, EstadoInventario) VALUES
(1, 1, 50, 1), -- Samsung Galaxy A54 en Metrocentro
(2, 1, 20, 1), -- iPhone 14 Pro en Metrocentro
(3, 2, 30, 1), -- Xiaomi Redmi Note 12 en León
(4, 3, 15, 1), -- Huawei Watch GT 3 en Granada
(5, 1, 100, 1), -- Funda Samsung A54 en Metrocentro
(6, 2, 25, 1); -- Motorola Edge 40 en León

-- 12. Inserción en Factura
INSERT INTO Factura (IdCliente, IdEmpleado, IdSucursal, FechaFactura, TotalFactura, EstadoFactura) VALUES
(1, 2, 1, '2025-06-20 10:30:00', 12800.00, 1), -- Factura para Juan Pérez en Metrocentro
(2, 1, 2, '2025-06-21 14:15:00', 6300.00, 1), -- Factura para Ana Sofía en León
(3, 3, 1, '2025-06-22 16:45:00', 35000.00, 1); -- Factura para Claudia en Metrocentro

-- 13. Inserción en DetalleFactura
INSERT INTO DetalleFactura (IdFactura, IdProducto, CantidadDetalle, PrecioUnitarioDetalle, SubtotalDetalle) VALUES
(1, 1, 1, 12500.00, 12500.00), -- Samsung Galaxy A54
(1, 5, 1, 300.00, 300.00), -- Funda Samsung A54
(2, 4, 1, 6000.00, 6000.00), -- Huawei Watch GT 3
(2, 5, 1, 300.00, 300.00), -- Funda
(3, 2, 1, 35000.00, 35000.00); -- iPhone 14 Pro