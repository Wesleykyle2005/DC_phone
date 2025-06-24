from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
import requests

# Create your views here.

# Vistas para Usuarios
class UsuarioListView(View):
    template_name = 'usuarios/usuario_list.html'

    def get(self, request):
        usuario = request.session.get('usuario')
        if not usuario:
            return redirect('usuarios:login')
        # Aquí deberías consumir la API para obtener la lista de usuarios si es necesario
        usuarios = []
        return render(request, self.template_name, {'usuarios': usuarios})

class UsuarioCreateView(View):
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:usuario-list')

    def get(self, request):
        usuario = request.session.get('usuario')
        if not usuario:
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request):
        # Aquí deberías consumir la API para crear un usuario
        return redirect(self.success_url)

class UsuarioUpdateView(View):
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:usuario-list')

    def get(self, request, pk):
        usuario = request.session.get('usuario')
        if not usuario:
            return redirect('usuarios:login')
        # Aquí deberías consumir la API para obtener el usuario a editar
        return render(request, self.template_name)

    def post(self, request, pk):
        # Aquí deberías consumir la API para actualizar el usuario
        return redirect(self.success_url)

class UsuarioDeleteView(View):
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuarios:usuario-list')

    def get(self, request, pk):
        usuario = request.session.get('usuario')
        if not usuario:
            return redirect('usuarios:login')
        # Aquí deberías consumir la API para obtener el usuario a eliminar
        return render(request, self.template_name)

    def post(self, request, pk):
        # Aquí deberías consumir la API para eliminar el usuario
        return redirect(self.success_url)

# Vistas de Autenticación
class CustomLogoutView(View):
    def post(self, request):
        request.session.flush()
        return redirect('usuarios:login')

class PersonaListCreateView(View):
    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        try:
            municipios_response = requests.get("https://dc-phone-api.onrender.com/api/Municipio", timeout=60)
            sucursales_response = requests.get("https://dc-phone-api.onrender.com/api/Sucursal", timeout=60)
            municipios = []
            sucursales = []
            if municipios_response.status_code == 200:
                municipios_api = municipios_response.json()
                municipios = [{'codigo_municipio': m.get('idMunicipio'), 'nombre_municipio': m.get('nombreMunicipio')} 
                            for m in municipios_api]
            if sucursales_response.status_code == 200:
                sucursales_api = sucursales_response.json()
                sucursales = [{'id': s.get('idSucursal'), 'nombre': s.get('nombreSucursal')} 
                            for s in sucursales_api if s.get('estadoSucursal', True)]
            # Cargar clientes o empleados según el filtro
            clientes_page = None
            empleados_page = None
            tipo_filtro = request.GET.get('tipo', 'cliente')
            search = request.GET.get('search', '')
            page = request.GET.get('page', 1)
            if tipo_filtro == 'empleado':
                # Cargar empleados
                empleados_response = requests.get("https://dc-phone-api.onrender.com/api/Empleado", timeout=60)
                if empleados_response.status_code == 200:
                    empleados_api = empleados_response.json()
                    # Mapear empleados con sus datos de persona
                    empleados = []
                    for empleado_api in empleados_api:
                        # Obtener datos de la persona asociada
                        persona_id = empleado_api.get('idPersona')
                        if persona_id:
                            persona_response = requests.get(f"https://dc-phone-api.onrender.com/api/Persona/{persona_id}", timeout=60)
                            if persona_response.status_code == 200:
                                persona_data = persona_response.json()
                                # Obtener datos de la sucursal
                                sucursal_id = empleado_api.get('idSucursal')
                                sucursal_nombre = 'N/A'
                                if sucursal_id:
                                    for sucursal in sucursales:
                                        if sucursal['id'] == sucursal_id:
                                            sucursal_nombre = sucursal['nombre']
                                            break
                                # Obtener datos del municipio
                                municipio_nombre = 'N/A'
                                municipio_id = persona_data.get('idMunicipio')
                                if municipio_id:
                                    for municipio in municipios:
                                        if municipio['codigo_municipio'] == municipio_id:
                                            municipio_nombre = municipio['nombre_municipio']
                                            break
                                empleado = {
                                    'id': empleado_api.get('idEmpleado'),
                                    'persona': {
                                        'dni': persona_data.get('dniPersona'),
                                        'nombre_completo': persona_data.get('nombreCompletoPersona'),
                                        'telefono': persona_data.get('telefonoPersona'),
                                        'codigo_municipio': {
                                            'nombre_municipio': municipio_nombre
                                        }
                                    },
                                    'id_sucursal': {
                                        'nombre': sucursal_nombre
                                    },
                                    'direccion': empleado_api.get('direccionEmpleado')
                                }
                                empleados.append(empleado)
                    # Aplicar búsqueda
                    if search:
                        empleados = [
                            e for e in empleados 
                            if search.lower() in e.get('persona', {}).get('nombre_completo', '').lower()
                        ]
                    # Simular paginación (en una implementación real, la API debería soportar paginación)
                    empleados_page = type('obj', (object,), {
                        'object_list': empleados,
                        'has_other_pages': False,
                        'has_previous': False,
                        'has_next': False,
                        'number': 1,
                        'paginator': type('obj', (object,), {'num_pages': 1, 'page_range': [1]})(),
                        'previous_page_number': None,
                        'next_page_number': None
                    })()
            else:
                # Cargar clientes
                clientes_response = requests.get("https://dc-phone-api.onrender.com/api/Cliente", timeout=60)
                if clientes_response.status_code == 200:
                    clientes_api = clientes_response.json()
                    # Mapear clientes con sus datos de persona
                    clientes = []
                    for cliente_api in clientes_api:
                        # Obtener datos de la persona asociada
                        persona_id = cliente_api.get('idPersona')
                        if persona_id:
                            persona_response = requests.get(f"https://dc-phone-api.onrender.com/api/Persona/{persona_id}", timeout=60)
                            if persona_response.status_code == 200:
                                persona_data = persona_response.json()
                                # Obtener datos del municipio
                                municipio_nombre = 'N/A'
                                municipio_id = persona_data.get('idMunicipio')
                                if municipio_id:
                                    for municipio in municipios:
                                        if municipio['codigo_municipio'] == municipio_id:
                                            municipio_nombre = municipio['nombre_municipio']
                                            break
                                cliente = {
                                    'id': cliente_api.get('idCliente'),
                                    'persona': {
                                        'dni': persona_data.get('dniPersona'),
                                        'nombre_completo': persona_data.get('nombreCompletoPersona'),
                                        'telefono': persona_data.get('telefonoPersona'),
                                        'codigo_municipio': {
                                            'nombre_municipio': municipio_nombre
                                        }
                                    }
                                }
                                clientes.append(cliente)
                    # Aplicar búsqueda
                    if search:
                        clientes = [
                            c for c in clientes 
                            if search.lower() in c.get('persona', {}).get('nombre_completo', '').lower()
                        ]
                    # Simular paginación
                    clientes_page = type('obj', (object,), {
                        'object_list': clientes,
                        'has_other_pages': False,
                        'has_previous': False,
                        'has_next': False,
                        'number': 1,
                        'paginator': type('obj', (object,), {'num_pages': 1, 'page_range': [1]})(),
                        'previous_page_number': None,
                        'next_page_number': None
                    })()
            return render(request, 'usuarios/persona_list.html', {
                'clientes_page': clientes_page,
                'empleados_page': empleados_page,
                'municipios': municipios,
                'sucursales': sucursales,
                'tipo_filtro': tipo_filtro,
                'search': search,
            })
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
            return render(request, 'usuarios/persona_list.html', {
                'clientes_page': None,
                'empleados_page': None,
                'municipios': [],
                'sucursales': [],
                'tipo_filtro': request.GET.get('tipo', 'cliente'),
                'search': request.GET.get('search', ''),
            })
        except Exception as e:
            messages.error(request, f'Error de conexión: {str(e)}')
            return render(request, 'usuarios/persona_list.html', {
                'clientes_page': None,
                'empleados_page': None,
                'municipios': [],
                'sucursales': [],
                'tipo_filtro': request.GET.get('tipo', 'cliente'),
                'search': request.GET.get('search', ''),
            })

    def post(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        try:
            dni = request.POST.get('dni')
            nombre_completo = request.POST.get('nombre_completo')
            telefono = request.POST.get('telefono')
            municipio_id = request.POST.get('municipio')
            tipo = request.POST.get('tipo')
            sucursal_id = request.POST.get('sucursal')
            direccion = request.POST.get('direccion')
            # Validar campos obligatorios
            if not (dni and nombre_completo and municipio_id and tipo):
                messages.error(request, 'Todos los campos obligatorios deben ser completados.')
                return redirect('usuarios:persona-list')
            # Crear persona primero
            persona_url = "https://dc-phone-api.onrender.com/api/Persona"
            persona_payload = {
                "dniPersona": dni,
                "nombreCompletoPersona": nombre_completo,
                "telefonoPersona": telefono or "",
                "idMunicipio": municipio_id,
                "estadoPersona": True
            }
            persona_response = requests.post(persona_url, json=persona_payload, timeout=60)
            if persona_response.status_code not in (200, 201, 204):
                messages.error(request, f'Error al crear persona: {persona_response.status_code}')
                return redirect('usuarios:persona-list')
            # Obtener el ID de la persona creada
            persona_data = persona_response.json()
            persona_id = persona_data.get('idPersona')
            if tipo == 'empleado':
                # Validar campos específicos de empleado
                if not (sucursal_id and direccion):
                    messages.error(request, 'Para empleados, sucursal y dirección son obligatorios.')
                    return redirect('usuarios:persona-list')
                # Crear empleado
                empleado_url = "https://dc-phone-api.onrender.com/api/Empleado"
                empleado_payload = {
                    "idPersona": persona_id,
                    "direccionEmpleado": direccion,
                    "idSucursal": int(sucursal_id)
                }
                empleado_response = requests.post(empleado_url, json=empleado_payload, timeout=60)
                if empleado_response.status_code in (200, 201, 204):
                    messages.success(request, f'Empleado "{nombre_completo}" creado exitosamente.')
                else:
                    messages.error(request, f'Error al crear empleado: {empleado_response.status_code}')
            else:
                # Crear cliente
                cliente_url = "https://dc-phone-api.onrender.com/api/Cliente"
                cliente_payload = {
                    "idPersona": persona_id
                }
                cliente_response = requests.post(cliente_url, json=cliente_payload, timeout=60)
                if cliente_response.status_code in (200, 201, 204):
                    messages.success(request, f'Cliente "{nombre_completo}" creado exitosamente.')
                else:
                    messages.error(request, f'Error al crear cliente: {cliente_response.status_code}')
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except ValueError:
            messages.error(request, 'Error: Los datos proporcionados no son válidos.')
        except Exception as e:
            messages.error(request, f'Error al crear {tipo}: {str(e)}')
        return redirect('usuarios:persona-list')

class PersonaDeleteView(View):
    success_url = reverse_lazy('usuarios:persona-list')

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            tipo = request.POST.get('tipo')
            
            if tipo == 'empleado':
                # Eliminar empleado
                url = f"https://dc-phone-api.onrender.com/api/Empleado/{pk}"
            else:
                # Eliminar cliente
                url = f"https://dc-phone-api.onrender.com/api/Cliente/{pk}"
            
            response = requests.delete(url, timeout=60)
            
            if response.status_code == 200:
                messages.success(request, f'{tipo.capitalize()} eliminado exitosamente.')
            else:
                messages.error(request, f'Error al eliminar {tipo}: {response.status_code}')
                
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except Exception as e:
            messages.error(request, f'Error al eliminar {tipo}: {str(e)}')
        
        return redirect(self.success_url)
