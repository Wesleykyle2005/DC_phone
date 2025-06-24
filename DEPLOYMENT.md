# 🚀 Guía de Despliegue - DC Phone Store

## Despliegue en Render

### Prerrequisitos
- Cuenta en [Render](https://render.com)
- Repositorio Git con el código del proyecto

### Pasos para el Despliegue

#### 1. Preparar el Repositorio
Asegúrate de que tu repositorio contenga todos los archivos necesarios:
- `Dockerfile`
- `render.yaml`
- `requirements.txt`
- `manage.py`
- Todos los archivos de la aplicación Django

#### 2. Crear un Nuevo Servicio en Render

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Haz clic en "New +" y selecciona "Blueprint"
3. Conecta tu repositorio Git
4. Render detectará automáticamente el `render.yaml` y configurará el servicio

#### 3. Configuración Automática

El archivo `render.yaml` configurará automáticamente:
- **Nombre del servicio**: `dc-phone-store`
- **Tipo**: Web Service
- **Plan**: Free
- **Variables de entorno**: Configuradas automáticamente
- **Health check**: En la ruta `/`

#### 4. Variables de Entorno (Opcional)

Si necesitas configurar variables adicionales, puedes hacerlo en el dashboard de Render:

```bash
# Variables recomendadas para producción
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=false
ALLOWED_HOSTS=.onrender.com,tu-dominio.com
```

#### 5. Despliegue Automático

Una vez configurado:
- Render construirá automáticamente tu aplicación
- Recolectará archivos estáticos
- Iniciará el servicio

### Verificación del Despliegue

1. **Health Check**: Render verificará automáticamente que tu aplicación responda en `/`
2. **Logs**: Revisa los logs en el dashboard de Render para detectar errores
3. **URL**: Tu aplicación estará disponible en `https://dc-phone-store.onrender.com`

### Solución de Problemas Comunes

#### Error de Archivos Estáticos
Si los archivos estáticos no se cargan:
```bash
python manage.py collectstatic --noinput
```

#### Error de Conexión a la API
Verifica que la API externa esté funcionando:
```bash
curl https://dc-phone-api.onrender.com/api/Usuario
```

### Comandos Útiles

#### Construir Localmente con Docker
```bash
docker build -t dc-phone-store .
docker run -p 8000:8000 dc-phone-store
```

#### Ejecutar Script de Build
```bash
chmod +x build.sh
./build.sh
```

#### Verificar Configuración Django
```bash
python manage.py check
```

### Estructura de Archivos para Despliegue

```
phone_store/
├── Dockerfile              # Configuración de Docker
├── render.yaml             # Configuración de Render
├── requirements.txt        # Dependencias de Python
├── build.sh                # Script de build
├── .dockerignore           # Archivos a ignorar en Docker
├── manage.py               # Script de gestión de Django
├── phone_store/            # Configuración principal de Django
│   ├── settings.py         # Configuración de la aplicación
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # Configuración WSGI
├── static/                 # Archivos estáticos
├── templates/              # Plantillas HTML
└── [apps]/                 # Aplicaciones Django
```

### Notas Importantes

1. **Base de Datos**: La aplicación NO requiere base de datos local ni migraciones. Todo el acceso a datos es vía API externa.
2. **Archivos Estáticos**: WhiteNoise se encarga de servir archivos estáticos en producción.
3. **Seguridad**: Las configuraciones de seguridad se activan automáticamente en producción.
4. **API Externa**: La aplicación consume datos de `https://dc-phone-api.onrender.com`.

### Soporte

Si encuentras problemas:
1. Revisa los logs en el dashboard de Render
2. Verifica la configuración de variables de entorno
3. Asegúrate de que todos los archivos estén en el repositorio
4. Contacta al equipo de desarrollo si el problema persiste 