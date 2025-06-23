#!/bin/bash

# Script de build para DC Phone Store
echo "🚀 Iniciando build de DC Phone Store..."

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: No se encontró manage.py. Asegúrate de estar en el directorio raíz del proyecto."
    exit 1
fi

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
python manage.py migrate

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Verificar que la aplicación funciona
echo "🔍 Verificando la aplicación..."
python manage.py check

echo "✅ Build completado exitosamente!"
echo "🎯 Para ejecutar en desarrollo: python manage.py runserver"
echo "🐳 Para construir Docker: docker build -t dc-phone-store ."
echo "🚀 Para ejecutar Docker: docker run -p 8000:8000 dc-phone-store" 