from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from .models import Inventario
from productos.models import Producto
from sucursales.models import Sucursal

# Create your views here.

# Vistas para Inventario
class InventarioListView(LoginRequiredMixin, ListView):
    model = Inventario
    template_name = 'inventario/inventario_list.html'
    context_object_name = 'inventarios'
    paginate_by = 10

    def get_queryset(self):
        queryset = Inventario.objects.filter(estado=True).order_by('producto__nombre')
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(producto__nombre__icontains=search_query) |
                Q(sucursal__nombre__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.all()
        context['sucursales'] = Sucursal.objects.all()
        return context

class InventarioCreateView(LoginRequiredMixin, CreateView):
    model = Inventario
    fields = ['producto', 'sucursal', 'cantidad']
    success_url = reverse_lazy('inventario:inventario-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.all()
        context['sucursales'] = Sucursal.objects.all()
        return context

    def form_valid(self, form):
        form.instance.estado = True
        messages.success(self.request, f'Inventario para "{form.instance.producto.nombre}" en sucursal "{form.instance.sucursal.nombre}" creado exitosamente.')
        return super().form_valid(form)

class InventarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Inventario
    success_url = reverse_lazy('inventario:inventario-list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = False
        self.object.save()
        messages.success(request, f'Inventario de "{self.object.producto.nombre}" en sucursal "{self.object.sucursal.nombre}" desactivado exitosamente.')
        return HttpResponseRedirect(self.get_success_url())
