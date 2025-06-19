from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Municipio, Rol
from productos.models import Marca, Categoria
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views

# Create your views here.

class MunicipioListView(LoginRequiredMixin, ListView):
    model = 'Municipio'  # Se actualizará cuando se cree el modelo
    context_object_name = 'municipios'
    template_name = 'core/municipio_list.html'

class MunicipioCreateView(LoginRequiredMixin, CreateView):
    model = 'Municipio'  # Se actualizará cuando se cree el modelo
    template_name = 'core/municipio_form.html'
    success_url = reverse_lazy('core:municipio-list')

class MunicipioUpdateView(LoginRequiredMixin, UpdateView):
    model = 'Municipio'  # Se actualizará cuando se cree el modelo
    template_name = 'core/municipio_form.html'
    success_url = reverse_lazy('core:municipio-list')

class MunicipioDeleteView(LoginRequiredMixin, DeleteView):
    model = 'Municipio'  # Se actualizará cuando se cree el modelo
    template_name = 'core/municipio_confirm_delete.html'
    success_url = reverse_lazy('core:municipio-list')

# Vistas para Roles
class RolListView(LoginRequiredMixin, ListView):
    model = 'Rol'  # Se actualizará cuando se cree el modelo
    context_object_name = 'roles'
    template_name = 'core/rol_list.html'

class RolCreateView(LoginRequiredMixin, CreateView):
    model = 'Rol'  # Se actualizará cuando se cree el modelo
    template_name = 'core/rol_form.html'
    success_url = reverse_lazy('core:rol-list')

class RolUpdateView(LoginRequiredMixin, UpdateView):
    model = 'Rol'  # Se actualizará cuando se cree el modelo
    template_name = 'core/rol_form.html'
    success_url = reverse_lazy('core:rol-list')

class RolDeleteView(LoginRequiredMixin, DeleteView):
    model = 'Rol'  # Se actualizará cuando se cree el modelo
    template_name = 'core/rol_confirm_delete.html'
    success_url = reverse_lazy('core:rol-list')

class OtrosListCreateView(View):
    def get(self, request):
        tipo = request.GET.get('tipo', 'municipio')
        search = request.GET.get('search', '')
        page = request.GET.get('page', 1)
        objetos = None
        nombre_campo = ''
        if tipo == 'rol':
            objetos = Rol.objects.all()
            nombre_campo = 'nombre_rol'
        elif tipo == 'marca':
            objetos = Marca.objects.all()
            nombre_campo = 'nombre'
        elif tipo == 'categoria':
            objetos = Categoria.objects.all()
            nombre_campo = 'nombre'
        else:
            tipo = 'municipio'
            objetos = Municipio.objects.all()
            nombre_campo = 'nombre_municipio'
        if search:
            objetos = objetos.filter(**{f"{nombre_campo}__icontains": search})
        paginator = Paginator(objetos, 10)
        page_obj = paginator.get_page(page)
        return render(request, 'core/otros_list.html', {
            'tipo': tipo,
            'search': search,
            'page_obj': page_obj,
        })

    def post(self, request):
        tipo = request.POST.get('tipo', 'municipio')
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        eliminar_id = request.POST.get('eliminar_id')
        if eliminar_id:
            if tipo == 'rol':
                Rol.objects.filter(id_rol=eliminar_id).delete()
                messages.success(request, 'Rol eliminado exitosamente.')
            elif tipo == 'marca':
                Marca.objects.filter(id=eliminar_id).delete()
                messages.success(request, 'Marca eliminada exitosamente.')
            elif tipo == 'categoria':
                Categoria.objects.filter(id=eliminar_id).delete()
                messages.success(request, 'Categoría eliminada exitosamente.')
            else:
                Municipio.objects.filter(codigo_municipio=eliminar_id).delete()
                messages.success(request, 'Municipio eliminado exitosamente.')
            return redirect(f"{request.path}?tipo={tipo}")
        if tipo == 'rol':
            if nombre:
                Rol.objects.create(nombre_rol=nombre)
                messages.success(request, 'Rol creado exitosamente.')
        elif tipo == 'marca':
            if nombre:
                Marca.objects.create(nombre=nombre)
                messages.success(request, 'Marca creada exitosamente.')
        elif tipo == 'categoria':
            if nombre:
                Categoria.objects.create(nombre=nombre)
                messages.success(request, 'Categoría creada exitosamente.')
        else:
            if nombre and codigo:
                Municipio.objects.create(codigo_municipio=codigo, nombre_municipio=nombre)
                messages.success(request, 'Municipio creado exitosamente.')
        return redirect(f"{request.path}?tipo={tipo}")

class WelcomeView(View):
    @method_decorator(login_required(login_url='usuarios:login'))
    def get(self, request):
        return render(request, 'welcome.html')

class CustomLoginView(auth_views.LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):
        from django.urls import reverse
        return reverse('core:welcome')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:welcome')
        return super().dispatch(request, *args, **kwargs)
