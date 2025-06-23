# Documentación de la API

Este documento fue generado automáticamente.

## Endpoints disponibles

| Método | Endpoint |
|--------|----------|

| GET | https://dc-phone-api.onrender.com/api/Municipio |

| GET | https://dc-phone-api.onrender.com/api/Municipio/{id} |

| POST | https://dc-phone-api.onrender.com/api/Municipio  |

| PUT | https://dc-phone-api.onrender.com/api/Municipio/{id}  |

| DELETE | https://dc-phone-api.onrender.com/api/Municipio/{id}  |

| GET | https://dc-phone-api.onrender.com/api/Rol |

| GET | https://dc-phone-api.onrender.com/api/Rol/{id} |

| POST | https://dc-phone-api.onrender.com/api/Rol  |

| PUT | https://dc-phone-api.onrender.com/api/Rol/{id}  |

| DELETE | https://dc-phone-api.onrender.com/api/Rol/{id}  |

| GET | https://dc-phone-api.onrender.com/api/Categoria |

| GET | https://dc-phone-api.onrender.com/api/Categoria/{id} |

| POST | https://dc-phone-api.onrender.com/api/Categoria  |

| PUT | https://dc-phone-api.onrender.com/api/Categoria/{id}  |

| DELETE | https://dc-phone-api.onrender.com/api/Categoria/{id}  |

| GET | https://dc-phone-api.onrender.com/api/Marca |

| GET | https://dc-phone-api.onrender.com/api/Marca/{id} |

| POST | https://dc-phone-api.onrender.com/api/Marca  |

| PUT | https://dc-phone-api.onrender.com/api/Marca/{id}  |

| DELETE | https://dc-phone-api.onrender.com/api/Marca/{id}  |

| GET | https://dc-phone-api.onrender.com/api/Sucursal |

| GET | https://dc-phone-api.onrender.com/api/Sucursal/{id} |

| POST | https://dc-phone-api.onrender.com/api/Sucursal  |

| PUT | https://dc-phone-api.onrender.com/api/Sucursal/{id}  |

| DELETE | https://dc-phone-api.onrender.com/api/Sucursal/{id}  |

| GET | https://dc-phone-api.onrender.com/api/Persona |

| GET | https://dc-phone-api.onrender.com/api/Persona/{id} |

| POST | https://dc-phone-api.onrender.com/api/Persona  |

| PUT | https://dc-phone-api.onrender.com/api/Persona/{id}  |

| DELETE | https://dc-phone-api.onrender.com/api/Persona/{id}  |

| GET | https://dc-phone-api.onrender.com/api/Producto |

| GET | https://dc-phone-api.onrender.com/api/Producto/{id} |

| POST | https://dc-phone-api.onrender.com/api/Producto  |

| PUT | https://dc-phone-api.onrender.com/api/Producto/{id}  |

| DELETE | https://dc-phone-api.onrender.com/api/Producto/{id}  |

| GET | https://dc-phone-api.onrender.com/api/Cliente |

| GET | https://dc-phone-api.onrender.com/api/Cliente/{id} |

| POST | https://dc-phone-api.onrender.com/api/Cliente  |

| PUT | https://dc-phone-api.onrender.com/api/Cliente/{id}  |

| DELETE | https://dc-phone-api.onrender.com/api/Cliente/{id}  |

| GET | https://dc-phone-api.onrender.com/api/Empleado |

| GET | https://dc-phone-api.onrender.com/api/Empleado/{id} |

| POST | https://dc-phone-api.onrender.com/api/Empleado  |

| PUT | https://dc-phone-api.onrender.com/api/Empleado/{id}  |

| DELETE | https://dc-phone-api.onrender.com/api/Empleado/{id}  |

| GET | https://dc-phone-api.onrender.com/api/Usuario |

| GET | https://dc-phone-api.onrender.com/api/Usuario/{id} |

| POST | https://dc-phone-api.onrender.com/api/Usuario  |

| PUT | https://dc-phone-api.onrender.com/api/Usuario/{id}  |

| DELETE | https://dc-phone-api.onrender.com/api/Usuario/{id}  |

| GET | https://dc-phone-api.onrender.com/api/Inventario |

| GET | https://dc-phone-api.onrender.com/api/Inventario/{id} |

| POST | https://dc-phone-api.onrender.com/api/Inventario  |

| PUT | https://dc-phone-api.onrender.com/api/Inventario/{id}  |

| DELETE | https://dc-phone-api.onrender.com/api/Inventario/{id}  |

| GET | https://dc-phone-api.onrender.com/api/Factura |

| GET | https://dc-phone-api.onrender.com/api/Factura/{id} |

| POST | https://dc-phone-api.onrender.com/api/Factura  |

| PUT | https://dc-phone-api.onrender.com/api/Factura/{id}  |

| DELETE | https://dc-phone-api.onrender.com/api/Factura/{id}  |

| GET | https://dc-phone-api.onrender.com/api/DetalleFactura |

| GET | https://dc-phone-api.onrender.com/api/DetalleFactura/{id} |

| POST | https://dc-phone-api.onrender.com/api/DetalleFactura  |

| PUT | https://dc-phone-api.onrender.com/api/DetalleFactura/{id}  |

| DELETE | https://dc-phone-api.onrender.com/api/DetalleFactura/{id}  |


---

## GET https://dc-phone-api.onrender.com/api/Municipio

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Municipio`


**Código de estado:** `200`


**Ejemplo de response:**

```json
[
  {
    "idMunicipio": "EKhhv",
    "nombreMunicipio": "Municipio ItgJL",
    "sucursales": [
      {
        "idSucursal": 1,
        "nombreSucursal": "Sucursal EmYYx",
        "direccionSucursal": "Direccion SAgMqSTe",
        "telefonoSucursal": "02671228",
        "idMunicipio": "EKhhv",
        "estadoSucursal": true,
        "municipio": null,
        "empleados": null,
        "inventarios": null,
        "facturas": null
      }
    ],
    "personas": [
      {
        "idPersona": 1,
        "dniPersona": "17397944",
        "nombreCompletoPersona": "Persona xMcOxl",
        "telefonoPersona": "86645189",
        "idMunicipio": "EKhhv",
        "estadoPersona": true,
        "municipio": null,
        "cliente": null,
        "empleado": null
      },
      {
        "idPersona": 2,
        "dniPersona": "79001890",
        "nombreCompletoPersona": "Persona OGxKLV",
        "telefonoPersona": "27577346",
        "idMunicipio": "EKhhv",
        "estadoPersona": true,
        "municipio": null,
        "cliente": null,
        "empleado": null
      }
    ]
  },
  {
    "idMunicipio": "qsyli",
    "nombreMunicipio": "Municipio irfJr",
    "sucursales": [],
    "personas": []
  }
]
```

---

## GET https://dc-phone-api.onrender.com/api/Municipio/EKhhv

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Municipio/EKhhv`


**Código de estado:** `200`


**Ejemplo de response:**

```json
{
  "idMunicipio": "EKhhv",
  "nombreMunicipio": "Municipio ItgJL",
  "sucursales": [
    {
      "idSucursal": 1,
      "nombreSucursal": "Sucursal EmYYx",
      "direccionSucursal": "Direccion SAgMqSTe",
      "telefonoSucursal": "02671228",
      "idMunicipio": "EKhhv",
      "estadoSucursal": true,
      "municipio": null,
      "empleados": null,
      "inventarios": null,
      "facturas": null
    }
  ],
  "personas": [
    {
      "idPersona": 1,
      "dniPersona": "17397944",
      "nombreCompletoPersona": "Persona xMcOxl",
      "telefonoPersona": "86645189",
      "idMunicipio": "EKhhv",
      "estadoPersona": true,
      "municipio": null,
      "cliente": null,
      "empleado": null
    },
    {
      "idPersona": 2,
      "dniPersona": "79001890",
      "nombreCompletoPersona": "Persona OGxKLV",
      "telefonoPersona": "27577346",
      "idMunicipio": "EKhhv",
      "estadoPersona": true,
      "municipio": null,
      "cliente": null,
      "empleado": null
    }
  ]
}
```

---

## POST https://dc-phone-api.onrender.com/api/Municipio 

**Método:** `POST`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Municipio `


**Ejemplo de request:**

```json
{
  "IdMunicipio": "EKhhv",
  "NombreMunicipio": "Municipio ItgJL",
  "idMunicipio": "EKhhv",
  "nombreMunicipio": "Municipio ItgJL",
  "sucursales": null,
  "personas": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
""
```

---

## PUT https://dc-phone-api.onrender.com/api/Municipio/EKhhv 

**Método:** `PUT`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Municipio/EKhhv `


**Ejemplo de request:**

```json
{
  "IdMunicipio": "EKhhv",
  "NombreMunicipio": "Municipio ItgJL",
  "idMunicipio": "EKhhv",
  "nombreMunicipio": "Municipio ItgJL",
  "sucursales": null,
  "personas": null
}
```

**Código de estado:** `400`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
  "title": "Bad Request",
  "status": 400,
  "traceId": "00-bcf8d5fb807d0504f3a365aaf82f2202-d6ff5ff6094717ed-00"
}
```

---

## DELETE https://dc-phone-api.onrender.com/api/Municipio/EKhhv 

**Método:** `DELETE`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Municipio/EKhhv `


**Código de estado:** `204`


**Ejemplo de response:**

```json
""
```

---

## GET https://dc-phone-api.onrender.com/api/Rol

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Rol`


**Código de estado:** `200`


**Ejemplo de response:**

```json
[
  {
    "idRol": 1,
    "nombreRol": "Rol fXTCE",
    "usuarios": null
  },
  {
    "idRol": 2,
    "nombreRol": "Rol DOvCU",
    "usuarios": null
  }
]
```

---

## GET https://dc-phone-api.onrender.com/api/Rol/2

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Rol/2`


**Código de estado:** `200`


**Ejemplo de response:**

```json
{
  "idRol": 2,
  "nombreRol": "Rol DOvCU",
  "usuarios": null
}
```

---

## POST https://dc-phone-api.onrender.com/api/Rol 

**Método:** `POST`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Rol `


**Ejemplo de request:**

```json
{
  "NombreRol": "Rol DOvCU",
  "idRol": 2,
  "nombreRol": "Rol DOvCU",
  "usuarios": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
""
```

---

## PUT https://dc-phone-api.onrender.com/api/Rol/2 

**Método:** `PUT`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Rol/2 `


**Ejemplo de request:**

```json
{
  "NombreRol": "Rol DOvCU",
  "idRol": 2,
  "nombreRol": "Rol DOvCU",
  "usuarios": null
}
```

**Código de estado:** `204`


**Ejemplo de response:**

```json
""
```

---

## DELETE https://dc-phone-api.onrender.com/api/Rol/2 

**Método:** `DELETE`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Rol/2 `


**Código de estado:** `204`


**Ejemplo de response:**

```json
""
```

---

## GET https://dc-phone-api.onrender.com/api/Categoria

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Categoria`


**Código de estado:** `200`


**Ejemplo de response:**

```json
[
  {
    "idCategoria": 1,
    "nombreCategoria": "Categoria pTRTr",
    "productos": null
  },
  {
    "idCategoria": 2,
    "nombreCategoria": "Categoria ntYzh",
    "productos": null
  }
]
```

---

## GET https://dc-phone-api.onrender.com/api/Categoria/2

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Categoria/2`


**Código de estado:** `200`


**Ejemplo de response:**

```json
{
  "idCategoria": 2,
  "nombreCategoria": "Categoria ntYzh",
  "productos": null
}
```

---

## POST https://dc-phone-api.onrender.com/api/Categoria 

**Método:** `POST`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Categoria `


**Ejemplo de request:**

```json
{
  "NombreCategoria": "Categoria ntYzh",
  "idCategoria": 2,
  "nombreCategoria": "Categoria ntYzh",
  "productos": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
""
```

---

## PUT https://dc-phone-api.onrender.com/api/Categoria/2 

**Método:** `PUT`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Categoria/2 `


**Ejemplo de request:**

```json
{
  "NombreCategoria": "Categoria ntYzh",
  "idCategoria": 2,
  "nombreCategoria": "Categoria ntYzh",
  "productos": null
}
```

**Código de estado:** `204`


**Ejemplo de response:**

```json
""
```

---

## DELETE https://dc-phone-api.onrender.com/api/Categoria/2 

**Método:** `DELETE`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Categoria/2 `


**Código de estado:** `204`


**Ejemplo de response:**

```json
""
```

---

## GET https://dc-phone-api.onrender.com/api/Marca

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Marca`


**Código de estado:** `200`


**Ejemplo de response:**

```json
[
  {
    "idMarca": 1,
    "nombreMarca": "Marca XRgVU",
    "productos": null
  }
]
```

---

## GET https://dc-phone-api.onrender.com/api/Marca/1

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Marca/1`


**Código de estado:** `200`


**Ejemplo de response:**

```json
{
  "idMarca": 1,
  "nombreMarca": "Marca XRgVU",
  "productos": null
}
```

---

## POST https://dc-phone-api.onrender.com/api/Marca 

**Método:** `POST`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Marca `


**Ejemplo de request:**

```json
{
  "NombreMarca": "Marca XRgVU",
  "idMarca": 1,
  "nombreMarca": "Marca XRgVU",
  "productos": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
""
```

---

## PUT https://dc-phone-api.onrender.com/api/Marca/1 

**Método:** `PUT`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Marca/1 `


**Ejemplo de request:**

```json
{
  "NombreMarca": "Marca XRgVU",
  "idMarca": 1,
  "nombreMarca": "Marca XRgVU",
  "productos": null
}
```

**Código de estado:** `204`


**Ejemplo de response:**

```json
""
```

---

## DELETE https://dc-phone-api.onrender.com/api/Marca/1 

**Método:** `DELETE`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Marca/1 `


**Código de estado:** `204`


**Ejemplo de response:**

```json
""
```

---

## GET https://dc-phone-api.onrender.com/api/Sucursal

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Sucursal`


**Código de estado:** `200`


**Ejemplo de response:**

```json
[]
```

---

## GET https://dc-phone-api.onrender.com/api/Sucursal/1

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Sucursal/1`


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-9e91e8725f8e0959ce17420208899108-7d591b2800adde3d-00"
}
```

---

## POST https://dc-phone-api.onrender.com/api/Sucursal 

**Método:** `POST`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Sucursal `


**Ejemplo de request:**

```json
{
  "NombreSucursal": "Sucursal EmYYx",
  "DireccionSucursal": "Direccion SAgMqSTe",
  "TelefonoSucursal": "02671228",
  "IdMunicipio": "EKhhv",
  "EstadoSucursal": true,
  "idSucursal": 1,
  "nombreSucursal": "Sucursal EmYYx",
  "direccionSucursal": "Direccion SAgMqSTe",
  "telefonoSucursal": "02671228",
  "idMunicipio": "EKhhv",
  "estadoSucursal": true,
  "municipio": null,
  "empleados": null,
  "inventarios": null,
  "facturas": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
""
```

---

## PUT https://dc-phone-api.onrender.com/api/Sucursal/1 

**Método:** `PUT`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Sucursal/1 `


**Ejemplo de request:**

```json
{
  "NombreSucursal": "Sucursal EmYYx",
  "DireccionSucursal": "Direccion SAgMqSTe",
  "TelefonoSucursal": "02671228",
  "IdMunicipio": "EKhhv",
  "EstadoSucursal": true,
  "idSucursal": 1,
  "nombreSucursal": "Sucursal EmYYx",
  "direccionSucursal": "Direccion SAgMqSTe",
  "telefonoSucursal": "02671228",
  "idMunicipio": "EKhhv",
  "estadoSucursal": true,
  "municipio": null,
  "empleados": null,
  "inventarios": null,
  "facturas": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-9b778603526efb7bc1f48d6e97a09b06-051ae85fee522642-00"
}
```

---

## DELETE https://dc-phone-api.onrender.com/api/Sucursal/1 

**Método:** `DELETE`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Sucursal/1 `


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-596249fe2a02da5e18605285b16e2bf2-bf1c639a22026d8e-00"
}
```

---

## GET https://dc-phone-api.onrender.com/api/Persona

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Persona`


**Código de estado:** `200`


**Ejemplo de response:**

```json
[]
```

---

## GET https://dc-phone-api.onrender.com/api/Persona/2

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Persona/2`


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-3ce4ca0365954f6f127e1a42acb5df1d-6dca5919bc3e4851-00"
}
```

---

## POST https://dc-phone-api.onrender.com/api/Persona 

**Método:** `POST`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Persona `


**Ejemplo de request:**

```json
{
  "DniPersona": "79001890",
  "NombreCompletoPersona": "Persona OGxKLV",
  "TelefonoPersona": "27577346",
  "IdMunicipio": "EKhhv",
  "EstadoPersona": true,
  "idPersona": 2,
  "dniPersona": "79001890",
  "nombreCompletoPersona": "Persona OGxKLV",
  "telefonoPersona": "27577346",
  "idMunicipio": "EKhhv",
  "estadoPersona": true,
  "municipio": null,
  "cliente": null,
  "empleado": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
""
```

---

## PUT https://dc-phone-api.onrender.com/api/Persona/2 

**Método:** `PUT`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Persona/2 `


**Ejemplo de request:**

```json
{
  "DniPersona": "79001890",
  "NombreCompletoPersona": "Persona OGxKLV",
  "TelefonoPersona": "27577346",
  "IdMunicipio": "EKhhv",
  "EstadoPersona": true,
  "idPersona": 2,
  "dniPersona": "79001890",
  "nombreCompletoPersona": "Persona OGxKLV",
  "telefonoPersona": "27577346",
  "idMunicipio": "EKhhv",
  "estadoPersona": true,
  "municipio": null,
  "cliente": null,
  "empleado": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-af664e1e556eaf3b818db3fb138ece5d-990013813c88322f-00"
}
```

---

## DELETE https://dc-phone-api.onrender.com/api/Persona/2 

**Método:** `DELETE`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Persona/2 `


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-8b9d74dd9157491ef1e216062f850f7e-00fa1be701a94ddf-00"
}
```

---

## GET https://dc-phone-api.onrender.com/api/Producto

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Producto`


**Código de estado:** `200`


**Ejemplo de response:**

```json
[]
```

---

## GET https://dc-phone-api.onrender.com/api/Producto/1

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Producto/1`


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-3fde43413e1a95890bad313647f5cdd8-913450ec2a4c5f6a-00"
}
```

---

## POST https://dc-phone-api.onrender.com/api/Producto 

**Método:** `POST`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Producto `


**Ejemplo de request:**

```json
{
  "NombreProducto": "Producto hbNyv",
  "DescripcionProducto": "Descripcion NkGsHYaxXB",
  "PrecioProducto": 78.69,
  "IdCategoria": 2,
  "IdMarca": 1,
  "EstadoProducto": true,
  "idProducto": 1,
  "nombreProducto": "Producto hbNyv",
  "descripcionProducto": "Descripcion NkGsHYaxXB",
  "precioProducto": 78.69,
  "idCategoria": 2,
  "idMarca": 1,
  "estadoProducto": true,
  "categoria": null,
  "marca": null,
  "inventarios": null,
  "detallesFactura": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
""
```

---

## PUT https://dc-phone-api.onrender.com/api/Producto/1 

**Método:** `PUT`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Producto/1 `


**Ejemplo de request:**

```json
{
  "NombreProducto": "Producto hbNyv",
  "DescripcionProducto": "Descripcion NkGsHYaxXB",
  "PrecioProducto": 78.69,
  "IdCategoria": 2,
  "IdMarca": 1,
  "EstadoProducto": true,
  "idProducto": 1,
  "nombreProducto": "Producto hbNyv",
  "descripcionProducto": "Descripcion NkGsHYaxXB",
  "precioProducto": 78.69,
  "idCategoria": 2,
  "idMarca": 1,
  "estadoProducto": true,
  "categoria": null,
  "marca": null,
  "inventarios": null,
  "detallesFactura": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-a6f5892db28f48a257a3adbfb19020aa-b31d7d3756ccffeb-00"
}
```

---

## DELETE https://dc-phone-api.onrender.com/api/Producto/1 

**Método:** `DELETE`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Producto/1 `


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-f2027877ade54c498828297f4662a543-23b2bba2b94e3301-00"
}
```

---

## GET https://dc-phone-api.onrender.com/api/Cliente

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Cliente`


**Código de estado:** `200`


**Ejemplo de response:**

```json
[]
```

---

## GET https://dc-phone-api.onrender.com/api/Cliente/1

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Cliente/1`


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-630531067884e584d46db8a2b088a467-781bd49d53994bab-00"
}
```

---

## POST https://dc-phone-api.onrender.com/api/Cliente 

**Método:** `POST`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Cliente `


**Ejemplo de request:**

```json
{
  "IdPersona": 2,
  "idCliente": 1,
  "idPersona": 2,
  "persona": null,
  "facturas": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
""
```

---

## PUT https://dc-phone-api.onrender.com/api/Cliente/1 

**Método:** `PUT`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Cliente/1 `


**Ejemplo de request:**

```json
{
  "IdPersona": 2,
  "idCliente": 1,
  "idPersona": 2,
  "persona": null,
  "facturas": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-24eb41a7a6c88629237aa8ce5b65acb1-23de950b2e5f8f36-00"
}
```

---

## DELETE https://dc-phone-api.onrender.com/api/Cliente/1 

**Método:** `DELETE`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Cliente/1 `


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-f27e61774fe2109ebf3ce8c14fe75ece-b9028e61938ac03a-00"
}
```

---

## GET https://dc-phone-api.onrender.com/api/Empleado

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Empleado`


**Código de estado:** `200`


**Ejemplo de response:**

```json
[]
```

---

## GET https://dc-phone-api.onrender.com/api/Empleado/1

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Empleado/1`


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-7fbaa0554805faf65060fe8adb50e1bc-5bdc2c600f4c18c4-00"
}
```

---

## POST https://dc-phone-api.onrender.com/api/Empleado 

**Método:** `POST`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Empleado `


**Ejemplo de request:**

```json
{
  "IdPersona": 1,
  "DireccionEmpleado": "Calle vcKSzhYp",
  "IdSucursal": 1,
  "idEmpleado": 1,
  "idPersona": 1,
  "direccionEmpleado": "Calle vcKSzhYp",
  "idSucursal": 1,
  "persona": null,
  "sucursal": null,
  "usuario": null,
  "facturas": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
""
```

---

## PUT https://dc-phone-api.onrender.com/api/Empleado/1 

**Método:** `PUT`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Empleado/1 `


**Ejemplo de request:**

```json
{
  "IdPersona": 1,
  "DireccionEmpleado": "Calle vcKSzhYp",
  "IdSucursal": 1,
  "idEmpleado": 1,
  "idPersona": 1,
  "direccionEmpleado": "Calle vcKSzhYp",
  "idSucursal": 1,
  "persona": null,
  "sucursal": null,
  "usuario": null,
  "facturas": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-608931da76607f83c417bf33ba9e593d-8cf00d6bc9e5cc63-00"
}
```

---

## DELETE https://dc-phone-api.onrender.com/api/Empleado/1 

**Método:** `DELETE`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Empleado/1 `


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-f2aebb26908b27c5421fc55be6874f13-fb91d99f589ae667-00"
}
```

---

## GET https://dc-phone-api.onrender.com/api/Usuario

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Usuario`


**Código de estado:** `200`


**Ejemplo de response:**

```json
[
  {
    "idUsuario": 1,
    "contrasenaUsuario": "YDBcBZNrKz",
    "ultimoInicioSesion": null,
    "esSuperUsuario": false,
    "nombreUsuario": "usuario_YjFDV",
    "nombre": "NombreYggY",
    "apellido": "ApellidogTvd",
    "correoElectronico": "xkqgwo@ejemplo.com",
    "esPersonal": false,
    "esActivo": true,
    "fechaRegistro": "2025-06-23T11:50:59",
    "idEmpleado": 1,
    "idRol": null,
    "estadoUsuario": true,
    "empleado": {
      "idEmpleado": 1,
      "idPersona": 0,
      "direccionEmpleado": "Calle vcKSzhYp",
      "idSucursal": 0,
      "persona": null,
      "sucursal": null,
      "usuario": null,
      "facturas": null
    },
    "rol": null
  }
]
```

---

## GET https://dc-phone-api.onrender.com/api/Usuario/1

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Usuario/1`


**Código de estado:** `200`


**Ejemplo de response:**

```json
{
  "idUsuario": 1,
  "contrasenaUsuario": "YDBcBZNrKz",
  "ultimoInicioSesion": null,
  "esSuperUsuario": false,
  "nombreUsuario": "usuario_YjFDV",
  "nombre": "NombreYggY",
  "apellido": "ApellidogTvd",
  "correoElectronico": "xkqgwo@ejemplo.com",
  "esPersonal": false,
  "esActivo": true,
  "fechaRegistro": "2025-06-23T11:50:59",
  "idEmpleado": 1,
  "idRol": null,
  "estadoUsuario": true,
  "empleado": {
    "idEmpleado": 1,
    "idPersona": 0,
    "direccionEmpleado": "Calle vcKSzhYp",
    "idSucursal": 0,
    "persona": null,
    "sucursal": null,
    "usuario": null,
    "facturas": null
  },
  "rol": null
}
```

---

## POST https://dc-phone-api.onrender.com/api/Usuario 

**Método:** `POST`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Usuario `


**Ejemplo de request:**

```json
{
  "ContrasenaUsuario": "YDBcBZNrKz",
  "NombreUsuario": "usuario_YjFDV",
  "Nombre": "NombreYggY",
  "Apellido": "ApellidogTvd",
  "CorreoElectronico": "xkqgwo@ejemplo.com",
  "EsSuperUsuario": false,
  "EsPersonal": false,
  "EsActivo": true,
  "FechaRegistro": "2025-06-23T11:50:59",
  "IdEmpleado": 1,
  "IdRol": 2,
  "EstadoUsuario": true,
  "idUsuario": 1,
  "contrasenaUsuario": "YDBcBZNrKz",
  "ultimoInicioSesion": null,
  "esSuperUsuario": false,
  "nombreUsuario": "usuario_YjFDV",
  "nombre": "NombreYggY",
  "apellido": "ApellidogTvd",
  "correoElectronico": "xkqgwo@ejemplo.com",
  "esPersonal": false,
  "esActivo": true,
  "fechaRegistro": "2025-06-23T11:50:59",
  "idEmpleado": 1,
  "idRol": 2,
  "estadoUsuario": true,
  "empleado": null,
  "rol": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
""
```

---

## PUT https://dc-phone-api.onrender.com/api/Usuario/1 

**Método:** `PUT`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Usuario/1 `


**Ejemplo de request:**

```json
{
  "ContrasenaUsuario": "YDBcBZNrKz",
  "NombreUsuario": "usuario_YjFDV",
  "Nombre": "NombreYggY",
  "Apellido": "ApellidogTvd",
  "CorreoElectronico": "xkqgwo@ejemplo.com",
  "EsSuperUsuario": false,
  "EsPersonal": false,
  "EsActivo": true,
  "FechaRegistro": "2025-06-23T11:50:59",
  "IdEmpleado": 1,
  "IdRol": 2,
  "EstadoUsuario": true,
  "idUsuario": 1,
  "contrasenaUsuario": "YDBcBZNrKz",
  "ultimoInicioSesion": null,
  "esSuperUsuario": false,
  "nombreUsuario": "usuario_YjFDV",
  "nombre": "NombreYggY",
  "apellido": "ApellidogTvd",
  "correoElectronico": "xkqgwo@ejemplo.com",
  "esPersonal": false,
  "esActivo": true,
  "fechaRegistro": "2025-06-23T11:50:59",
  "idEmpleado": 1,
  "idRol": 2,
  "estadoUsuario": true,
  "empleado": null,
  "rol": null
}
```

**Código de estado:** `500`


**Ejemplo de response:**

```json
""
```

---

## DELETE https://dc-phone-api.onrender.com/api/Usuario/1 

**Método:** `DELETE`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Usuario/1 `


**Código de estado:** `204`


**Ejemplo de response:**

```json
""
```

---

## GET https://dc-phone-api.onrender.com/api/Inventario

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Inventario`


**Código de estado:** `200`


**Ejemplo de response:**

```json
[]
```

---

## GET https://dc-phone-api.onrender.com/api/Inventario/1

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Inventario/1`


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-4831c89a301fbc66b523854a92fd66f3-d1992bd531200917-00"
}
```

---

## POST https://dc-phone-api.onrender.com/api/Inventario 

**Método:** `POST`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Inventario `


**Ejemplo de request:**

```json
{
  "IdProducto": 1,
  "IdSucursal": 1,
  "CantidadInventario": 31,
  "EstadoInventario": true,
  "idInventario": 1,
  "idProducto": 1,
  "idSucursal": 1,
  "cantidadInventario": 31,
  "estadoInventario": true,
  "producto": null,
  "sucursal": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
""
```

---

## PUT https://dc-phone-api.onrender.com/api/Inventario/1 

**Método:** `PUT`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Inventario/1 `


**Ejemplo de request:**

```json
{
  "IdProducto": 1,
  "IdSucursal": 1,
  "CantidadInventario": 31,
  "EstadoInventario": true,
  "idInventario": 1,
  "idProducto": 1,
  "idSucursal": 1,
  "cantidadInventario": 31,
  "estadoInventario": true,
  "producto": null,
  "sucursal": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-6b70f6e7b7078b54d0cea9222b4fd52b-66cc6f1affe18719-00"
}
```

---

## DELETE https://dc-phone-api.onrender.com/api/Inventario/1 

**Método:** `DELETE`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Inventario/1 `


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-fa5d1c1c42761d2e3df4bdd43345972c-42afb3a8ac59ebd8-00"
}
```

---

## GET https://dc-phone-api.onrender.com/api/Factura

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Factura`


**Código de estado:** `200`


**Ejemplo de response:**

```json
[]
```

---

## GET https://dc-phone-api.onrender.com/api/Factura/1

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Factura/1`


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-7c5303e9de74d15bd83fe9b9ffeb6147-1e15ac7b92dba903-00"
}
```

---

## POST https://dc-phone-api.onrender.com/api/Factura 

**Método:** `POST`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Factura `


**Ejemplo de request:**

```json
{
  "IdCliente": 1,
  "IdEmpleado": 1,
  "IdSucursal": 1,
  "FechaFactura": "2025-06-23T11:50:57",
  "TotalFactura": 586.87,
  "EstadoFactura": true,
  "idFactura": 1,
  "idCliente": 1,
  "idEmpleado": 1,
  "idSucursal": 1,
  "fechaFactura": "2025-06-23T11:50:57",
  "totalFactura": 586.87,
  "estadoFactura": true,
  "cliente": null,
  "empleado": null,
  "sucursal": null,
  "detallesFactura": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
""
```

---

## PUT https://dc-phone-api.onrender.com/api/Factura/1 

**Método:** `PUT`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Factura/1 `


**Ejemplo de request:**

```json
{
  "IdCliente": 1,
  "IdEmpleado": 1,
  "IdSucursal": 1,
  "FechaFactura": "2025-06-23T11:50:57",
  "TotalFactura": 586.87,
  "EstadoFactura": true,
  "idFactura": 1,
  "idCliente": 1,
  "idEmpleado": 1,
  "idSucursal": 1,
  "fechaFactura": "2025-06-23T11:50:57",
  "totalFactura": 586.87,
  "estadoFactura": true,
  "cliente": null,
  "empleado": null,
  "sucursal": null,
  "detallesFactura": null
}
```

**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-ada7edbe28ce73a3caed2925f8ccff51-3c4239dabbe098b4-00"
}
```

---

## DELETE https://dc-phone-api.onrender.com/api/Factura/1 

**Método:** `DELETE`


**Endpoint:** `https://dc-phone-api.onrender.com/api/Factura/1 `


**Código de estado:** `404`


**Ejemplo de response:**

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-134d11e310ed1bd9ef8429653986cfb9-4119506ee43ffbbb-00"
}
```

---

## GET https://dc-phone-api.onrender.com/api/DetalleFactura

**Método:** `GET`


**Endpoint:** `https://dc-phone-api.onrender.com/api/DetalleFactura`


**Código de estado:** `200`


**Ejemplo de response:**

```json
[]
```

---

## POST https://dc-phone-api.onrender.com/api/DetalleFactura 

**Método:** `POST`


**Endpoint:** `https://dc-phone-api.onrender.com/api/DetalleFactura `


**Código de estado:** `404`


**Ejemplo de response:**

```json
""
```

---
