from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from personas.models import Persona, Cliente, Empleado
from sucursales.models import Sucursal
from core.models import Municipio
from django.core.paginator import Paginator

# Create your views here.

# Vistas para Usuarios
class UsuarioListView(LoginRequiredMixin, ListView):
    model = 'Usuario'  # Se actualizará cuando se cree el modelo
    context_object_name = 'usuarios'
    template_name = 'usuarios/usuario_list.html'

    def get_queryset(self):
        # Aquí se puede personalizar la consulta
        # Por ejemplo: filtrar por rol, estado, etc.
        return super().get_queryset()

class UsuarioCreateView(LoginRequiredMixin, CreateView):
    model = 'Usuario'  # Se actualizará cuando se cree el modelo
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:usuario-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí se pueden agregar datos adicionales al contexto
        # Por ejemplo: listas de empleados, roles disponibles
        return context

class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = 'Usuario'  # Se actualizará cuando se cree el modelo
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:usuario-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí se pueden agregar datos adicionales al contexto
        return context

class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = 'Usuario'  # Se actualizará cuando se cree el modelo
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuarios:usuario-list')

# Vistas de Autenticación
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('usuarios:login')
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response

class PersonaListCreateView(View):
    def get(self, request):
        tipo_filtro = request.GET.get('tipo', 'cliente')
        search = request.GET.get('search', '')
        page = request.GET.get('page', 1)
        if tipo_filtro == 'empleado':
            empleados = Empleado.objects.select_related('persona', 'id_sucursal').filter(persona__estado=True)
            if search:
                empleados = empleados.filter(persona__nombre_completo__icontains=search)
            paginator = Paginator(empleados, 10)
            empleados_page = paginator.get_page(page)
            clientes_page = None
        else:
            clientes = Cliente.objects.select_related('persona').filter(persona__estado=True)
            if search:
                clientes = clientes.filter(persona__nombre_completo__icontains=search)
            paginator = Paginator(clientes, 10)
            clientes_page = paginator.get_page(page)
            empleados_page = None
        municipios = Municipio.objects.all()
        sucursales = Sucursal.objects.filter(estado=True)
        return render(request, 'usuarios/persona_list.html', {
            'clientes_page': clientes_page,
            'empleados_page': empleados_page,
            'municipios': municipios,
            'sucursales': sucursales,
            'tipo_filtro': tipo_filtro,
            'search': search,
        })

    def post(self, request):
        dni = request.POST.get('dni')
        nombre_completo = request.POST.get('nombre_completo')
        telefono = request.POST.get('telefono')
        municipio_id = request.POST.get('municipio')
        tipo = request.POST.get('tipo')
        sucursal_id = request.POST.get('sucursal')
        direccion = request.POST.get('direccion')
        if not (dni and nombre_completo and municipio_id and tipo):
            messages.error(request, 'Todos los campos obligatorios deben ser completados.')
            return redirect('usuarios:persona-list')
        persona = Persona.objects.create(
            dni=dni,
            nombre_completo=nombre_completo,
            telefono=telefono,
            codigo_municipio_id=municipio_id,
            estado=True
        )
        if tipo == 'cliente':
            Cliente.objects.create(persona=persona)
            messages.success(request, f'Cliente "{nombre_completo}" creado exitosamente.')
        elif tipo == 'empleado':
            if not (sucursal_id and direccion):
                messages.error(request, 'Debe especificar sucursal y dirección para empleados.')
                persona.delete()
                return redirect('usuarios:persona-list')
            Empleado.objects.create(persona=persona, direccion=direccion, id_sucursal_id=sucursal_id)
            messages.success(request, f'Empleado "{nombre_completo}" creado exitosamente.')
        else:
            persona.delete()
            messages.error(request, 'Tipo de persona no válido.')
        return redirect('usuarios:persona-list')
