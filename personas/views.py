from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# Vistas para Clientes
class ClienteListView(LoginRequiredMixin, ListView):
    model = 'Cliente'  # Se actualizará cuando se cree el modelo
    context_object_name = 'clientes'
    template_name = 'personas/cliente_list.html'

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = 'Cliente'  # Se actualizará cuando se cree el modelo
    template_name = 'personas/cliente_form.html'
    success_url = reverse_lazy('personas:cliente-list')

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = 'Cliente'  # Se actualizará cuando se cree el modelo
    template_name = 'personas/cliente_form.html'
    success_url = reverse_lazy('personas:cliente-list')

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = 'Cliente'  # Se actualizará cuando se cree el modelo
    template_name = 'personas/cliente_confirm_delete.html'
    success_url = reverse_lazy('personas:cliente-list')

# Vistas para Empleados
class EmpleadoListView(LoginRequiredMixin, ListView):
    model = 'Empleado'  # Se actualizará cuando se cree el modelo
    context_object_name = 'empleados'
    template_name = 'personas/empleado_list.html'

class EmpleadoCreateView(LoginRequiredMixin, CreateView):
    model = 'Empleado'  # Se actualizará cuando se cree el modelo
    template_name = 'personas/empleado_form.html'
    success_url = reverse_lazy('personas:empleado-list')

class EmpleadoUpdateView(LoginRequiredMixin, UpdateView):
    model = 'Empleado'  # Se actualizará cuando se cree el modelo
    template_name = 'personas/empleado_form.html'
    success_url = reverse_lazy('personas:empleado-list')

class EmpleadoDeleteView(LoginRequiredMixin, DeleteView):
    model = 'Empleado'  # Se actualizará cuando se cree el modelo
    template_name = 'personas/empleado_confirm_delete.html'
    success_url = reverse_lazy('personas:empleado-list')
