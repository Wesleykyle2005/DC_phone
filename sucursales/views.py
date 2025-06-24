from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
import requests

# Create your views here.

# Vistas para Sucursales
class SucursalListView(View):
    template_name = 'sucursales/sucursal_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        url = "https://dc-phone-api.onrender.com/api/Sucursal"
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                sucursales_api = response.json()
                sucursales = []
                for s in sucursales_api:
                    if s.get('estadoSucursal', True):
                        sucursal = {
                            'id': s.get('idSucursal'),
                            'nombre': s.get('nombreSucursal'),
                            'direccion': s.get('direccionSucursal'),
                            'telefono': s.get('telefonoSucursal'),
                            'estado': s.get('estadoSucursal'),
                            'municipio': {
                                'nombre_municipio': s.get('municipio', {}).get('nombreMunicipio', 'N/A'),
                                'codigo_municipio': s.get('municipio', {}).get('idMunicipio', '')
                            }
                        }
                        sucursales.append(sucursal)
                # Búsqueda
                search_query = request.GET.get('search', '')
                if search_query:
                    sucursales = [
                        s for s in sucursales
                        if (search_query.lower() in s.get('nombre', '').lower() or
                            search_query.lower() in s.get('direccion', '').lower() or
                            search_query.lower() in s.get('telefono', '').lower() or
                            search_query.lower() in s.get('municipio', {}).get('nombre_municipio', '').lower())
                    ]
                # Cargar municipios para el modal
                municipios = []
                try:
                    municipios_response = requests.get("https://dc-phone-api.onrender.com/api/Municipio", timeout=60)
                    if municipios_response.status_code == 200:
                        municipios_api = municipios_response.json()
                        municipios = [
                            {
                                'codigo_municipio': m.get('idMunicipio'),
                                'nombre_municipio': m.get('nombreMunicipio')
                            }
                            for m in municipios_api if m.get('estadoMunicipio', True)
                        ]
                except Exception as e:
                    print(f"Error cargando municipios: {e}")
                return render(request, self.template_name, {
                    'sucursales': sucursales,
                    'search_query': search_query,
                    'municipios': municipios
                })
            else:
                messages.error(request, f'Error al cargar sucursales: {response.status_code}')
                return render(request, self.template_name, {
                    'sucursales': [],
                    'municipios': []
                })
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
            return render(request, self.template_name, {
                'sucursales': [],
                'municipios': []
            })
        except Exception as e:
            messages.error(request, f'Error de conexión: {str(e)}')
            return render(request, self.template_name, {
                'sucursales': [],
                'municipios': []
            })

class SucursalCreateView(View):
    success_url = reverse_lazy('sucursales:sucursal-list')

    def post(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        try:
            nombre = request.POST.get('nombre')
            direccion = request.POST.get('direccion')
            telefono = request.POST.get('telefono')
            municipio_id = request.POST.get('municipio')
            if not all([nombre, direccion, municipio_id]):
                messages.error(request, 'Todos los campos obligatorios deben ser completados.')
                return redirect('sucursales:sucursal-list')
            url = "https://dc-phone-api.onrender.com/api/Sucursal"
            payload = {
                "nombreSucursal": nombre,
                "direccionSucursal": direccion,
                "telefonoSucursal": telefono or "",
                "idMunicipio": municipio_id,
                "estadoSucursal": True
            }
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code in (200, 201, 204):
                messages.success(request, f'Sucursal "{nombre}" creada exitosamente.')
            else:
                messages.error(request, f'Error al crear sucursal: {response.status_code}')
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except Exception as e:
            messages.error(request, f'Error al crear sucursal: {str(e)}')
        return redirect(self.success_url)

class SucursalDeleteView(View):
    success_url = reverse_lazy('sucursales:sucursal-list')

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        try:
            url = f"https://dc-phone-api.onrender.com/api/Sucursal/{pk}"
            response = requests.delete(url, timeout=60)
            if response.status_code == 200:
                messages.success(request, 'Sucursal eliminada exitosamente.')
            else:
                messages.error(request, f'Error al eliminar sucursal: {response.status_code}')
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except Exception as e:
            messages.error(request, f'Error al eliminar sucursal: {str(e)}')
        return redirect(self.success_url)
