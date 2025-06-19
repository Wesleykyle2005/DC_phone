from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from .models import Sucursal
from core.models import Municipio

# Create your views here.

# Vistas para Sucursales
class SucursalListView(LoginRequiredMixin, ListView):
    model = Sucursal
    template_name = 'sucursales/sucursal_list.html'
    context_object_name = 'sucursales'
    paginate_by = 10

    def get_queryset(self):
        queryset = Sucursal.objects.filter(estado=True).order_by('nombre')
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query) |
                Q(direccion__icontains=search_query) |
                Q(telefono__icontains=search_query) |
                Q(municipio__nombre_municipio__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['municipios'] = Municipio.objects.all()
        return context

class SucursalCreateView(LoginRequiredMixin, CreateView):
    model = Sucursal
    fields = ['nombre', 'direccion', 'telefono', 'municipio']
    success_url = reverse_lazy('sucursales:sucursal-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['municipios'] = Municipio.objects.all()
        return context

    def form_valid(self, form):
        form.instance.estado = True
        messages.success(self.request, f'La sucursal "{form.instance.nombre}" ha sido creada exitosamente.')
        return super().form_valid(form)

class SucursalDeleteView(LoginRequiredMixin, DeleteView):
    model = Sucursal
    success_url = reverse_lazy('sucursales:sucursal-list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = False
        self.object.save()
        messages.success(request, f'La sucursal "{self.object.nombre}" ha sido desactivada exitosamente.')
        return HttpResponseRedirect(self.get_success_url())
