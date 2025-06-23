from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.

# Vistas para Clientes
class ClienteListView(View):
    template_name = 'personas/cliente_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        # Aquí deberías consumir la API para obtener clientes
        clientes = []
        return render(request, self.template_name, {'clientes': clientes})

class ClienteCreateView(View):
    template_name = 'personas/cliente_form.html'
    success_url = reverse_lazy('personas:cliente-list')

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request):
        # Aquí deberías consumir la API para crear cliente
        return redirect(self.success_url)

class ClienteUpdateView(View):
    template_name = 'personas/cliente_form.html'
    success_url = reverse_lazy('personas:cliente-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request, pk):
        # Aquí deberías consumir la API para actualizar cliente
        return redirect(self.success_url)

class ClienteDeleteView(View):
    template_name = 'personas/cliente_confirm_delete.html'
    success_url = reverse_lazy('personas:cliente-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request, pk):
        # Aquí deberías consumir la API para eliminar cliente
        return redirect(self.success_url)

# Vistas para Empleados
class EmpleadoListView(View):
    template_name = 'personas/empleado_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        # Aquí deberías consumir la API para obtener empleados
        empleados = []
        return render(request, self.template_name, {'empleados': empleados})

class EmpleadoCreateView(View):
    template_name = 'personas/empleado_form.html'
    success_url = reverse_lazy('personas:empleado-list')

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request):
        # Aquí deberías consumir la API para crear empleado
        return redirect(self.success_url)

class EmpleadoUpdateView(View):
    template_name = 'personas/empleado_form.html'
    success_url = reverse_lazy('personas:empleado-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request, pk):
        # Aquí deberías consumir la API para actualizar empleado
        return redirect(self.success_url)

class EmpleadoDeleteView(View):
    template_name = 'personas/empleado_confirm_delete.html'
    success_url = reverse_lazy('personas:empleado-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request, pk):
        # Aquí deberías consumir la API para eliminar empleado
        return redirect(self.success_url)
