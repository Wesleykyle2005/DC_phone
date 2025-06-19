from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from .models import Producto, Categoria, Marca

# Create your views here.

# Vistas para Productos
class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'
    paginate_by = 10

    def get_queryset(self):
        queryset = Producto.objects.filter(estado=True).order_by('nombre')
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query) |
                Q(descripcion__icontains=search_query) |
                Q(marca__nombre__icontains=search_query) |
                Q(categoria__nombre__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['marcas'] = Marca.objects.all()
        return context

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    fields = ['nombre', 'descripcion', 'precio', 'categoria', 'marca']
    success_url = reverse_lazy('productos:producto-list')

    def form_valid(self, form):
        form.instance.estado = True
        messages.success(self.request, f'El producto "{form.instance.nombre}" ha sido creado exitosamente.')
        return super().form_valid(form)

class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    success_url = reverse_lazy('productos:producto-list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = False
        self.object.save()
        messages.success(request, f'El producto "{self.object.nombre}" ha sido desactivado exitosamente.')
        return HttpResponseRedirect(self.get_success_url())
