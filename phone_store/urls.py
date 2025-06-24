"""phone_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic import TemplateView

def redirect_to_login(request):
    if request.session.get('usuario'):
        return redirect('core:welcome')
    return redirect('usuarios:login')

urlpatterns = [
    # path('admin/', admin.site.urls),  # Eliminado porque no hay admin
    path('', redirect_to_login),  # Redirige la raíz al login
    path('welcome/', TemplateView.as_view(template_name='welcome.html'), name='welcome'),
    path('core/', include('core.urls')),
    path('ventas/', include('ventas.urls')),
    path('inventario/', include('inventario.urls')),
    path('sucursales/', include('sucursales.urls')),
    path('productos/', include('productos.urls')),
    path('personas/', include('personas.urls')),
    path('usuarios/', include('usuarios.urls')),
]
