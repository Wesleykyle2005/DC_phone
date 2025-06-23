from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Municipio, Rol
from productos.models import Marca, Categoria
import requests

# Create your views here.

class MunicipioListView(View):
    template_name = 'core/municipio_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        # Aquí deberías consumir la API para obtener municipios
        municipios = []
        return render(request, self.template_name, {'municipios': municipios})

class MunicipioCreateView(View):
    template_name = 'core/municipio_form.html'
    success_url = reverse_lazy('core:municipio-list')

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request):
        # Aquí deberías consumir la API para crear municipio
        return redirect(self.success_url)

class MunicipioUpdateView(View):
    template_name = 'core/municipio_form.html'
    success_url = reverse_lazy('core:municipio-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request, pk):
        # Aquí deberías consumir la API para actualizar municipio
        return redirect(self.success_url)

class MunicipioDeleteView(View):
    template_name = 'core/municipio_confirm_delete.html'
    success_url = reverse_lazy('core:municipio-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request, pk):
        # Aquí deberías consumir la API para eliminar municipio
        return redirect(self.success_url)

# Vistas para Roles
class RolListView(View):
    template_name = 'core/rol_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        # Aquí deberías consumir la API para obtener roles
        roles = []
        return render(request, self.template_name, {'roles': roles})

class RolCreateView(View):
    template_name = 'core/rol_form.html'
    success_url = reverse_lazy('core:rol-list')

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request):
        # Aquí deberías consumir la API para crear rol
        return redirect(self.success_url)

class RolUpdateView(View):
    template_name = 'core/rol_form.html'
    success_url = reverse_lazy('core:rol-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request, pk):
        # Aquí deberías consumir la API para actualizar rol
        return redirect(self.success_url)

class RolDeleteView(View):
    template_name = 'core/rol_confirm_delete.html'
    success_url = reverse_lazy('core:rol-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request, pk):
        # Aquí deberías consumir la API para eliminar rol
        return redirect(self.success_url)

class OtrosListCreateView(View):
    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        tipo = request.GET.get('tipo', 'municipio')
        search = request.GET.get('search', '')
        page = request.GET.get('page', 1)
        # Aquí deberías consumir la API para obtener los datos según el tipo
        objetos = []
        page_obj = None
        return render(request, 'core/otros_list.html', {
            'tipo': tipo,
            'search': search,
            'page_obj': page_obj,
        })

    def post(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        tipo = request.POST.get('tipo', 'municipio')
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        eliminar_id = request.POST.get('eliminar_id')
        # Aquí deberías consumir la API para crear o eliminar según el tipo
        if eliminar_id:
            messages.success(request, f'{tipo.capitalize()} eliminado exitosamente.')
        elif nombre:
            messages.success(request, f'{tipo.capitalize()} creado exitosamente.')
        return redirect(f"{request.path}?tipo={tipo}")

class WelcomeView(View):
    def get(self, request):
        print(f"DEBUG: Session usuario: {request.session.get('usuario')}")
        print(f"DEBUG: Session keys: {list(request.session.keys())}")
        if not request.session.get('usuario'):
            print("DEBUG: No usuario en sesión, redirigiendo a login")
            return redirect('usuarios:login')
        print("DEBUG: Usuario encontrado en sesión")
        return render(request, 'welcome.html')

class CustomLoginView(View):
    template_name = 'usuarios/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"DEBUG: Intentando login con usuario: {username}")
        url = "https://dc-phone-api.onrender.com/api/Usuario"
        response = requests.get(url)
        if response.status_code == 200:
            usuarios = response.json()
            usuario = next(
                (u for u in usuarios if u.get('nombreUsuario') == username and u.get('contrasenaUsuario') == password),
                None
            )
            if usuario:
                print(f"DEBUG: Usuario encontrado: {usuario.get('nombreUsuario')}")
                request.session['usuario'] = usuario
                print(f"DEBUG: Usuario guardado en sesión: {request.session.get('usuario')}")
                return redirect('core:welcome')
            else:
                print("DEBUG: Usuario no encontrado en la API")
        else:
            print(f"DEBUG: Error en API: {response.status_code}")
        messages.error(request, 'Usuario o contraseña incorrectos.')
        return render(request, self.template_name)
