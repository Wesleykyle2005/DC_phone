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