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
    success_url = reverse_lazy('usuarios:persona-list')

    def get(self, request):
        usuario = request.session.get('usuario')
        if not usuario:
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        try:
            nombre_usuario = request.POST.get('nombreUsuario')
            contrasena_usuario = request.POST.get('contrasenaUsuario')
            id_empleado = request.POST.get('idEmpleado')
            # Nuevos campos
            nombre = request.POST.get('empleado_nombre', '')
            apellido = request.POST.get('apellido', '')
            correo = request.POST.get('correo', '')
            id_rol = request.POST.get('idRol', 1)
            es_activo = 1
            es_personal = 1
            fecha_registro = None
            from datetime import datetime
            fecha_registro = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            es_superusuario = 0
            ultimo_inicio = None
            # Validar campos obligatorios
            campos_faltantes = []
            if not nombre_usuario:
                campos_faltantes.append('nombre de usuario')
            if not contrasena_usuario:
                campos_faltantes.append('contraseña')
            if not id_empleado:
                campos_faltantes.append('empleado')
            if not apellido:
                campos_faltantes.append('apellido')
            if not correo:
                campos_faltantes.append('correo electrónico')
            if not id_rol or str(id_rol) == '0':
                campos_faltantes.append('rol')
            if campos_faltantes:
                messages.error(request, f'Todos los campos son obligatorios para crear el usuario. Faltan: {", ".join(campos_faltantes)}')
                return redirect('usuarios:persona-list')
            url = "https://dc-phone-api.onrender.com/api/Usuario"
            payload = {
                "NombreUsuario": nombre_usuario,
                "contrasenaUsuario": contrasena_usuario,
                "idEmpleado": int(id_empleado),
                "estadoUsuario": True,
                "Nombre": nombre,
                "Apellido": apellido,
                "CorreoElectronico": correo,
                "IdRol": int(id_rol),
                "EsActivo": True,
                "EsPersonal": True,
                "FechaRegistro": fecha_registro,
                "EsSuperUsuario": False,
                "UltimoInicioSesion": ultimo_inicio
            }
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code in (200, 201, 204):
                messages.success(request, f'Usuario "{nombre_usuario}" creado exitosamente.')
            else:
                messages.error(request, f'Error al crear usuario: {response.status_code} - {response.text}')
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except Exception as e:
            messages.error(request, f'Error al crear usuario: {str(e)}')
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
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        try:
            tipo = request.POST.get('tipo')
            if tipo == 'empleado':
                # Intentar eliminar cliente asociado primero (si existe)
                try:
                    cliente_url = f"https://dc-phone-api.onrender.com/api/Cliente/{pk}"
                    requests.delete(cliente_url, timeout=30)
                except Exception as e:
                    print(f"No se pudo eliminar cliente asociado: {e}")
                # Luego eliminar empleado
                url = f"https://dc-phone-api.onrender.com/api/Empleado/{pk}"
                response = requests.delete(url, timeout=60)
            else:
                # Eliminar cliente
                url = f"https://dc-phone-api.onrender.com/api/Cliente/{pk}"
                response = requests.delete(url, timeout=60)
            if response.status_code in (200, 204):
                messages.success(request, f'{tipo.capitalize()} eliminado exitosamente.')
            else:
                messages.error(request, f'Error al eliminar {tipo}: {response.status_code}')
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except Exception as e:
            messages.error(request, f'Error al eliminar {tipo}: {str(e)}')
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
                usuarios_response = requests.get("https://dc-phone-api.onrender.com/api/Usuario", timeout=60)
                usuarios_api = usuarios_response.json() if usuarios_response.status_code == 200 else []
                if empleados_response.status_code == 200:
                    empleados_api = empleados_response.json()
                    # Mapear empleados con sus datos de persona
                    empleados = []
                    for empleado_api in empleados_api:
                        # Obtener datos de la persona asociada
                        persona_id = empleado_api.get('idPersona')
                        usuario_empleado = next((u for u in usuarios_api if u.get('idEmpleado') == empleado_api.get('idEmpleado')), None)
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
                                        'id': persona_data.get('idPersona'),
                                        'dni': persona_data.get('dniPersona'),
                                        'nombre_completo': persona_data.get('nombreCompletoPersona'),
                                        'telefono': persona_data.get('telefonoPersona'),
                                        'estado': persona_data.get('estadoPersona', True),
                                        'codigo_municipio': {
                                            'codigo_municipio': municipio_id,
                                            'nombre_municipio': municipio_nombre
                                        }
                                    },
                                    'id_sucursal': {
                                        'id': sucursal_id,
                                        'nombre': sucursal_nombre
                                    },
                                    'direccion': empleado_api.get('direccionEmpleado'),
                                    'usuario': usuario_empleado
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
                                        'id': persona_data.get('idPersona'),
                                        'dni': persona_data.get('dniPersona'),
                                        'nombre_completo': persona_data.get('nombreCompletoPersona'),
                                        'telefono': persona_data.get('telefonoPersona'),
                                        'estado': persona_data.get('estadoPersona', True),
                                        'codigo_municipio': {
                                            'codigo_municipio': municipio_id,
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
            # Cargar roles para el modal de usuario
            roles = []
            try:
                roles_response = requests.get("https://dc-phone-api.onrender.com/api/Rol", timeout=60)
                if roles_response.status_code == 200:
                    roles_api = roles_response.json()
                    roles = [{'id': r.get('idRol'), 'nombre': r.get('nombreRol')} for r in roles_api if r.get('estadoRol', True)]
            except Exception as e:
                print(f"Error cargando roles: {e}")
            return render(request, 'usuarios/persona_list.html', {
                'clientes_page': clientes_page,
                'empleados_page': empleados_page,
                'municipios': municipios,
                'sucursales': sucursales,
                'roles': roles,
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
            accion = request.POST.get('accion')
            if accion == 'editar_empleado':
                # Edición de empleado
                id_persona = request.POST.get('id_persona')
                id_empleado = request.POST.get('id_empleado')
                dni = request.POST.get('dni')
                nombre_completo = request.POST.get('nombre_completo')
                telefono = request.POST.get('telefono')
                municipio_id = request.POST.get('municipio')
                direccion = request.POST.get('direccion')
                sucursal_id = request.POST.get('sucursal')
                estado = request.POST.get('estado') == '1'
                # Actualizar persona
                persona_url = f"https://dc-phone-api.onrender.com/api/Persona/{id_persona}"
                persona_payload = {
                    "idPersona": int(id_persona),
                    "dniPersona": dni,
                    "nombreCompletoPersona": nombre_completo,
                    "telefonoPersona": telefono or "",
                    "idMunicipio": municipio_id,
                    "estadoPersona": estado
                }
                persona_response = requests.put(persona_url, json=persona_payload, timeout=60)
                if persona_response.status_code not in (200, 204):
                    messages.error(request, f'Error al actualizar persona: {persona_response.status_code} - {persona_response.text}')
                    return redirect('usuarios:persona-list')
                # Actualizar empleado
                empleado_url = f"https://dc-phone-api.onrender.com/api/Empleado/{id_empleado}"
                empleado_payload = {
                    "idEmpleado": int(id_empleado),
                    "idPersona": int(id_persona),
                    "direccionEmpleado": direccion,
                    "idSucursal": int(sucursal_id)
                }
                empleado_response = requests.put(empleado_url, json=empleado_payload, timeout=60)
                if empleado_response.status_code in (200, 204):
                    messages.success(request, 'Empleado actualizado exitosamente.')
                else:
                    messages.error(request, f'Error al actualizar empleado: {empleado_response.status_code} - {empleado_response.text}')
                return redirect('usuarios:persona-list')
            elif accion == 'editar_cliente':
                # Edición de cliente
                id_persona = request.POST.get('id_persona')
                id_cliente = request.POST.get('id_cliente')
                dni = request.POST.get('dni')
                nombre_completo = request.POST.get('nombre_completo')
                telefono = request.POST.get('telefono')
                municipio_id = request.POST.get('municipio')
                estado = request.POST.get('estado') == '1'
                # Actualizar persona
                persona_url = f"https://dc-phone-api.onrender.com/api/Persona/{id_persona}"
                persona_payload = {
                    "idPersona": int(id_persona),
                    "dniPersona": dni,
                    "nombreCompletoPersona": nombre_completo,
                    "telefonoPersona": telefono or "",
                    "idMunicipio": municipio_id,
                    "estadoPersona": estado
                }
                persona_response = requests.put(persona_url, json=persona_payload, timeout=60)
                if persona_response.status_code not in (200, 204):
                    messages.error(request, f'Error al actualizar persona: {persona_response.status_code} - {persona_response.text}')
                    return redirect('usuarios:persona-list')
                # Actualizar cliente
                cliente_url = f"https://dc-phone-api.onrender.com/api/Cliente/{id_cliente}"
                cliente_payload = {
                    "idCliente": int(id_cliente),
                    "idPersona": int(id_persona)
                }
                cliente_response = requests.put(cliente_url, json=cliente_payload, timeout=60)
                if cliente_response.status_code in (200, 204):
                    messages.success(request, 'Cliente actualizado exitosamente.')
                else:
                    messages.error(request, f'Error al actualizar cliente: {cliente_response.status_code} - {cliente_response.text}')
                return redirect('usuarios:persona-list')
            elif accion == 'editar_usuario':
                # Edición de usuario
                id_usuario = request.POST.get('id_usuario')
                id_empleado = request.POST.get('id_empleado')
                nombre_usuario = request.POST.get('nombre_usuario')
                contrasena = request.POST.get('contrasena')
                nombre = request.POST.get('nombre')
                apellido = request.POST.get('apellido')
                correo = request.POST.get('correo')
                rol = request.POST.get('rol')
                estado_usuario = request.POST.get('estado_usuario') == '1'
                
                # Construir payload para usuario
                usuario_payload = {
                    "idUsuario": int(id_usuario),
                    "nombreUsuario": nombre_usuario,
                    "contrasenaUsuario": contrasena,
                    "nombre": nombre,
                    "apellido": apellido,
                    "correoElectronico": correo,
                    "idEmpleado": int(id_empleado),
                    "idRol": int(rol),
                    "estadoUsuario": estado_usuario,
                    "esActivo": True,
                    "esPersonal": True,
                    "esSuperUsuario": False
                }
                
                # Actualizar usuario
                usuario_url = f"https://dc-phone-api.onrender.com/api/Usuario/{id_usuario}"
                usuario_response = requests.put(usuario_url, json=usuario_payload, timeout=60)
                if usuario_response.status_code in (200, 204):
                    messages.success(request, 'Usuario actualizado exitosamente.')
                else:
                    messages.error(request, f'Error al actualizar usuario: {usuario_response.status_code} - {usuario_response.text}')
                return redirect('usuarios:persona-list')
            # Cargar municipios para validación
            municipios_response = requests.get("https://dc-phone-api.onrender.com/api/Municipio", timeout=60)
            municipios = []
            if municipios_response.status_code == 200:
                municipios_api = municipios_response.json()
                municipios = [{'codigo_municipio': m.get('idMunicipio'), 'nombre_municipio': m.get('nombreMunicipio')} 
                              for m in municipios_api]
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
            # Validar municipio
            municipios_validos = [str(m['codigo_municipio']) for m in municipios]
            if municipio_id not in municipios_validos:
                messages.error(request, 'El municipio seleccionado no es válido o ha sido eliminado.')
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
                messages.error(request, f'Error al crear persona: {persona_response.status_code} - {persona_response.text}')
                return redirect('usuarios:persona-list')
            # Obtener el ID de la persona creada
            persona_data = persona_response.json()
            persona_id = persona_data.get('idPersona')
            if not persona_id:
                messages.error(request, 'No se pudo obtener el ID de la persona creada.')
                return redirect('usuarios:persona-list')
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
                    try:
                        error_msg = empleado_response.json()
                    except Exception:
                        error_msg = empleado_response.text
                    messages.error(request, f'Error al crear empleado: {empleado_response.status_code} - {error_msg}')
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
                    try:
                        error_msg = cliente_response.json()
                    except Exception:
                        error_msg = cliente_response.text
                    messages.error(request, f'Error al crear cliente: {cliente_response.status_code} - {error_msg}')
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
            
            if response.status_code in (200, 204):
                messages.success(request, f'{tipo.capitalize()} eliminado exitosamente.')
            else:
                messages.error(request, f'Error al eliminar {tipo}: {response.status_code}')
                
        except requests.Timeout:
            messages.error(request, 'Timeout: La API tardó demasiado en responder.')
        except Exception as e:
            messages.error(request, f'Error al eliminar {tipo}: {str(e)}')
        
        return redirect(self.success_url)
