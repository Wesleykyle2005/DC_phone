from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
import requests

# Configuración de la API
API_BASE_URL = 'https://dc-phone-api.onrender.com/api'

def get_api_data(endpoint, params=None):
    """Función helper para obtener datos de la API"""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}", params=params, timeout=60)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error obteniendo datos de {endpoint}: {e}")
        return []

def post_api_data(endpoint, data):
    """Función helper para enviar datos a la API"""
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data, timeout=60)
        return response.status_code in (200, 201, 204)
    except Exception as e:
        print(f"Error enviando datos a {endpoint}: {e}")
        return False

def put_api_data(endpoint, data):
    """Función helper para actualizar datos en la API"""
    try:
        response = requests.put(f"{API_BASE_URL}/{endpoint}", json=data, timeout=60)
        return response.status_code == 200 or response.status_code == 204
    except Exception as e:
        print(f"Error actualizando datos en {endpoint}: {e}")
        return False

def delete_api_data(endpoint):
    """Función helper para eliminar datos de la API"""
    try:
        response = requests.delete(f"{API_BASE_URL}/{endpoint}", timeout=60)
        return response.status_code == 200 or response.status_code == 204
    except Exception as e:
        print(f"Error eliminando datos de {endpoint}: {e}")
        return False

# Create your views here.

class MunicipioListView(View):
    template_name = 'core/municipio_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        # Obtener municipios de la API
        municipios = get_api_data('Municipio')
        
        # Aplicar búsqueda
        search = request.GET.get('search', '')
        if search:
            municipios = [m for m in municipios if search.lower() in m.get('nombreMunicipio', '').lower()]
        
        # Paginación
        paginator = Paginator(municipios, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'municipios': page_obj,
            'search': search,
        }
        return render(request, self.template_name, context)

class MunicipioCreateView(View):
    template_name = 'core/municipio_form.html'
    success_url = reverse_lazy('core:municipio-list')

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            codigo_municipio = request.POST.get('codigo_municipio')
            nombre_municipio = request.POST.get('nombre_municipio')
            
            if not codigo_municipio or not nombre_municipio:
                messages.error(request, 'Todos los campos son obligatorios.')
                return render(request, self.template_name)
            
            municipio_data = {
                'idMunicipio': codigo_municipio,
                'nombreMunicipio': nombre_municipio
            }
            
            if post_api_data('Municipio', municipio_data):
                messages.success(request, 'Municipio creado exitosamente.')
                return redirect(self.success_url)
            else:
                messages.error(request, 'Error al crear el municipio.')
                return render(request, self.template_name)
                
        except Exception as e:
            print(f"Error en creación de municipio: {e}")
            messages.error(request, 'Error interno del servidor.')
            return render(request, self.template_name)

class MunicipioUpdateView(View):
    template_name = 'core/municipio_form.html'
    success_url = reverse_lazy('core:municipio-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        municipio = get_api_data(f'Municipio/{pk}')
        if not municipio:
            messages.error(request, 'Municipio no encontrado.')
            return redirect('core:municipio-list')
        
        context = {'municipio': municipio}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            codigo_municipio = request.POST.get('codigo_municipio')
            nombre_municipio = request.POST.get('nombre_municipio')
            
            if not codigo_municipio or not nombre_municipio:
                messages.error(request, 'Todos los campos son obligatorios.')
                return render(request, self.template_name)
            
            municipio_data = {
                'idMunicipio': codigo_municipio,
                'nombreMunicipio': nombre_municipio
            }
            
            if put_api_data(f'Municipio/{pk}', municipio_data):
                messages.success(request, 'Municipio actualizado exitosamente.')
                return redirect(self.success_url)
            else:
                messages.error(request, 'Error al actualizar el municipio.')
                return render(request, self.template_name)
                
        except Exception as e:
            print(f"Error en actualización de municipio: {e}")
            messages.error(request, 'Error interno del servidor.')
            return render(request, self.template_name)

class MunicipioDeleteView(View):
    template_name = 'core/municipio_confirm_delete.html'
    success_url = reverse_lazy('core:municipio-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        municipio = get_api_data(f'Municipio/{pk}')
        if not municipio:
            messages.error(request, 'Municipio no encontrado.')
            return redirect('core:municipio-list')
        
        context = {'municipio': municipio}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        if delete_api_data(f'Municipio/{pk}'):
            messages.success(request, 'Municipio eliminado exitosamente.')
        else:
            messages.error(request, 'Error al eliminar el municipio.')
        
        return redirect(self.success_url)

# Vistas para Roles
class RolListView(View):
    template_name = 'core/rol_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        # Obtener roles de la API
        roles = get_api_data('Rol')
        
        # Aplicar búsqueda
        search = request.GET.get('search', '')
        if search:
            roles = [r for r in roles if search.lower() in r.get('nombreRol', '').lower()]
        
        # Paginación
        paginator = Paginator(roles, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'roles': page_obj,
            'search': search,
        }
        return render(request, self.template_name, context)

class RolCreateView(View):
    template_name = 'core/rol_form.html'
    success_url = reverse_lazy('core:rol-list')

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            nombre_rol = request.POST.get('nombre_rol')
            
            if not nombre_rol:
                messages.error(request, 'El nombre del rol es obligatorio.')
                return render(request, self.template_name)
            
            rol_data = {
                'nombreRol': nombre_rol
            }
            
            if post_api_data('Rol', rol_data):
                messages.success(request, 'Rol creado exitosamente.')
                return redirect(self.success_url)
            else:
                messages.error(request, 'Error al crear el rol.')
                return render(request, self.template_name)
                
        except Exception as e:
            print(f"Error en creación de rol: {e}")
            messages.error(request, 'Error interno del servidor.')
            return render(request, self.template_name)

class RolUpdateView(View):
    template_name = 'core/rol_form.html'
    success_url = reverse_lazy('core:rol-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        rol = get_api_data(f'Rol/{pk}')
        if not rol:
            messages.error(request, 'Rol no encontrado.')
            return redirect('core:rol-list')
        
        context = {'rol': rol}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            nombre_rol = request.POST.get('nombre_rol')
            
            if not nombre_rol:
                messages.error(request, 'El nombre del rol es obligatorio.')
                return render(request, self.template_name)
            
            rol_data = {
                'nombreRol': nombre_rol
            }
            
            if put_api_data(f'Rol/{pk}', rol_data):
                messages.success(request, 'Rol actualizado exitosamente.')
                return redirect(self.success_url)
            else:
                messages.error(request, 'Error al actualizar el rol.')
                return render(request, self.template_name)
                
        except Exception as e:
            print(f"Error en actualización de rol: {e}")
            messages.error(request, 'Error interno del servidor.')
            return render(request, self.template_name)

class RolDeleteView(View):
    template_name = 'core/rol_confirm_delete.html'
    success_url = reverse_lazy('core:rol-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        rol = get_api_data(f'Rol/{pk}')
        if not rol:
            messages.error(request, 'Rol no encontrado.')
            return redirect('core:rol-list')
        
        context = {'rol': rol}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        if delete_api_data(f'Rol/{pk}'):
            messages.success(request, 'Rol eliminado exitosamente.')
        else:
            messages.error(request, 'Error al eliminar el rol.')
        
        return redirect(self.success_url)

# Vistas para Marcas
class MarcaListView(View):
    template_name = 'core/marca_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        # Obtener marcas de la API
        marcas = get_api_data('Marca')
        
        # Aplicar búsqueda
        search = request.GET.get('search', '')
        if search:
            marcas = [m for m in marcas if search.lower() in m.get('nombreMarca', '').lower()]
        
        # Paginación
        paginator = Paginator(marcas, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'marcas': page_obj,
            'search': search,
        }
        return render(request, self.template_name, context)

class MarcaCreateView(View):
    template_name = 'core/marca_form.html'
    success_url = reverse_lazy('core:marca-list')

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            nombre_marca = request.POST.get('nombre_marca')
            
            if not nombre_marca:
                messages.error(request, 'El nombre de la marca es obligatorio.')
                return render(request, self.template_name)
            
            marca_data = {
                'nombreMarca': nombre_marca
            }
            
            if post_api_data('Marca', marca_data):
                messages.success(request, 'Marca creada exitosamente.')
                return redirect(self.success_url)
            else:
                messages.error(request, 'Error al crear la marca.')
                return render(request, self.template_name)
                
        except Exception as e:
            print(f"Error en creación de marca: {e}")
            messages.error(request, 'Error interno del servidor.')
            return render(request, self.template_name)

class MarcaUpdateView(View):
    template_name = 'core/marca_form.html'
    success_url = reverse_lazy('core:marca-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        marca = get_api_data(f'Marca/{pk}')
        if not marca:
            messages.error(request, 'Marca no encontrada.')
            return redirect('core:marca-list')
        
        context = {'marca': marca}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            nombre_marca = request.POST.get('nombre_marca')
            
            if not nombre_marca:
                messages.error(request, 'El nombre de la marca es obligatorio.')
                return render(request, self.template_name)
            
            marca_data = {
                'nombreMarca': nombre_marca
            }
            
            if put_api_data(f'Marca/{pk}', marca_data):
                messages.success(request, 'Marca actualizada exitosamente.')
                return redirect(self.success_url)
            else:
                messages.error(request, 'Error al actualizar la marca.')
                return render(request, self.template_name)
                
        except Exception as e:
            print(f"Error en actualización de marca: {e}")
            messages.error(request, 'Error interno del servidor.')
            return render(request, self.template_name)

class MarcaDeleteView(View):
    template_name = 'core/marca_confirm_delete.html'
    success_url = reverse_lazy('core:marca-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        marca = get_api_data(f'Marca/{pk}')
        if not marca:
            messages.error(request, 'Marca no encontrada.')
            return redirect('core:marca-list')
        
        context = {'marca': marca}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        if delete_api_data(f'Marca/{pk}'):
            messages.success(request, 'Marca eliminada exitosamente.')
        else:
            messages.error(request, 'Error al eliminar la marca.')
        
        return redirect(self.success_url)

# Vistas para Categorías
class CategoriaListView(View):
    template_name = 'core/categoria_list.html'

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        # Obtener categorías de la API
        categorias = get_api_data('Categoria')
        
        # Aplicar búsqueda
        search = request.GET.get('search', '')
        if search:
            categorias = [c for c in categorias if search.lower() in c.get('nombreCategoria', '').lower()]
        
        # Paginación
        paginator = Paginator(categorias, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'categorias': page_obj,
            'search': search,
        }
        return render(request, self.template_name, context)

class CategoriaCreateView(View):
    template_name = 'core/categoria_form.html'
    success_url = reverse_lazy('core:categoria-list')

    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        return render(request, self.template_name)

    def post(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            nombre_categoria = request.POST.get('nombre_categoria')
            
            if not nombre_categoria:
                messages.error(request, 'El nombre de la categoría es obligatorio.')
                return render(request, self.template_name)
            
            categoria_data = {
                'nombreCategoria': nombre_categoria
            }
            
            if post_api_data('Categoria', categoria_data):
                messages.success(request, 'Categoría creada exitosamente.')
                return redirect(self.success_url)
            else:
                messages.error(request, 'Error al crear la categoría.')
                return render(request, self.template_name)
                
        except Exception as e:
            print(f"Error en creación de categoría: {e}")
            messages.error(request, 'Error interno del servidor.')
            return render(request, self.template_name)

class CategoriaUpdateView(View):
    template_name = 'core/categoria_form.html'
    success_url = reverse_lazy('core:categoria-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        categoria = get_api_data(f'Categoria/{pk}')
        if not categoria:
            messages.error(request, 'Categoría no encontrada.')
            return redirect('core:categoria-list')
        
        context = {'categoria': categoria}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        try:
            nombre_categoria = request.POST.get('nombre_categoria')
            
            if not nombre_categoria:
                messages.error(request, 'El nombre de la categoría es obligatorio.')
                return render(request, self.template_name)
            
            categoria_data = {
                'nombreCategoria': nombre_categoria
            }
            
            if put_api_data(f'Categoria/{pk}', categoria_data):
                messages.success(request, 'Categoría actualizada exitosamente.')
                return redirect(self.success_url)
            else:
                messages.error(request, 'Error al actualizar la categoría.')
                return render(request, self.template_name)
                
        except Exception as e:
            print(f"Error en actualización de categoría: {e}")
            messages.error(request, 'Error interno del servidor.')
            return render(request, self.template_name)

class CategoriaDeleteView(View):
    template_name = 'core/categoria_confirm_delete.html'
    success_url = reverse_lazy('core:categoria-list')

    def get(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        categoria = get_api_data(f'Categoria/{pk}')
        if not categoria:
            messages.error(request, 'Categoría no encontrada.')
            return redirect('core:categoria-list')
        
        context = {'categoria': categoria}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        
        if delete_api_data(f'Categoria/{pk}'):
            messages.success(request, 'Categoría eliminada exitosamente.')
        else:
            messages.error(request, 'Error al eliminar la categoría.')
        
        return redirect(self.success_url)

class OtrosListCreateView(View):
    def get(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        tipo = request.GET.get('tipo', 'municipio')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        objetos = []
        # Obtener datos según el tipo
        if tipo == 'municipio':
            municipios = get_api_data('Municipio')
            for m in municipios:
                if not search or search.lower() in m.get('nombreMunicipio', '').lower():
                    objetos.append({
                        'codigo_municipio': m.get('idMunicipio'),
                        'nombre_municipio': m.get('nombreMunicipio')
                    })
        elif tipo == 'rol':
            roles = get_api_data('Rol')
            for r in roles:
                if not search or search.lower() in r.get('nombreRol', '').lower():
                    objetos.append({
                        'id_rol': r.get('idRol'),
                        'nombre_rol': r.get('nombreRol')
                    })
        elif tipo == 'marca':
            marcas = get_api_data('Marca')
            for m in marcas:
                if not search or search.lower() in m.get('nombreMarca', '').lower():
                    objetos.append({
                        'id': m.get('idMarca'),
                        'nombre': m.get('nombreMarca')
                    })
        elif tipo == 'categoria':
            categorias = get_api_data('Categoria')
            for c in categorias:
                if not search or search.lower() in c.get('nombreCategoria', '').lower():
                    objetos.append({
                        'id': c.get('idCategoria'),
                        'nombre': c.get('nombreCategoria')
                    })
        # Paginación
        page_size = 10
        total = len(objetos)
        start = (page - 1) * page_size
        end = start + page_size
        page_obj = objetos[start:end]
        # Simular objeto de paginación para la plantilla
        from django.core.paginator import Paginator, Page
        paginator = Paginator(objetos, page_size)
        page_obj = paginator.get_page(page)
        return render(request, 'core/otros_list.html', {
            'tipo': tipo,
            'search': search,
            'page_obj': page_obj,
        })

    def post(self, request):
        if not request.session.get('usuario'):
            return redirect('usuarios:login')
        tipo = request.POST.get('tipo', 'municipio')
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        eliminar_id = request.POST.get('eliminar_id')
        success = False
        error = None
        # Crear o eliminar según el tipo
        try:
            if eliminar_id:
                if tipo == 'municipio':
                    success = delete_api_data(f'Municipio/{eliminar_id}')
                elif tipo == 'rol':
                    success = delete_api_data(f'Rol/{eliminar_id}')
                elif tipo == 'marca':
                    success = delete_api_data(f'Marca/{eliminar_id}')
                elif tipo == 'categoria':
                    success = delete_api_data(f'Categoria/{eliminar_id}')
                if success:
                    messages.success(request, f'{tipo.capitalize()} eliminado exitosamente.')
                else:
                    messages.error(request, f'Error al eliminar el {tipo}.')
            elif nombre:
                if tipo == 'municipio':
                    if not codigo:
                        messages.error(request, 'El código es obligatorio para municipio.')
                        return redirect(f"{request.path}?tipo={tipo}")
                    data = {'idMunicipio': codigo, 'nombreMunicipio': nombre}
                    success = post_api_data('Municipio', data)
                elif tipo == 'rol':
                    data = {'nombreRol': nombre}
                    success = post_api_data('Rol', data)
                elif tipo == 'marca':
                    data = {'nombreMarca': nombre}
                    success = post_api_data('Marca', data)
                elif tipo == 'categoria':
                    data = {'nombreCategoria': nombre}
                    success = post_api_data('Categoria', data)
                if success:
                    messages.success(request, f'{tipo.capitalize()} creado exitosamente.')
                else:
                    messages.error(request, f'Error al crear el {tipo}.')
        except Exception as e:
            messages.error(request, f'Error interno: {e}')
        return redirect(f"{request.path}?tipo={tipo}")

class WelcomeView(View):
    def get(self, request):
        print(f"DEBUG: Session usuario: {request.session.get('usuario')}")
        print(f"DEBUG: Session keys: {list(request.session.keys())}")
        if not request.session.get('usuario'):
            print("DEBUG: No usuario en sesión, redirigiendo a login")
            return redirect('usuarios:login')
        print("DEBUG: Usuario encontrado en sesión")
        return render(request, 'welcome.html')

class CustomLoginView(View):
    template_name = 'usuarios/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"DEBUG: Intentando login con usuario: {username}")
        url = "https://dc-phone-api.onrender.com/api/Usuario"
        response = requests.get(url)
        if response.status_code == 200:
            usuarios = response.json()
            usuario = next(
                (u for u in usuarios if u.get('nombreUsuario') == username and u.get('contrasenaUsuario') == password),
                None
            )
            if usuario:
                print(f"DEBUG: Usuario encontrado: {usuario.get('nombreUsuario')}")
                request.session['usuario'] = usuario
                print(f"DEBUG: Usuario guardado en sesión: {request.session.get('usuario')}")
                return redirect('core:welcome')
            else:
                print("DEBUG: Usuario no encontrado en la API")
        else:
            print(f"DEBUG: Error en API: {response.status_code}")
        messages.error(request, 'Usuario o contraseña incorrectos.')
        return render(request, self.template_name)
