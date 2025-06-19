import os
import sys

# Ruta absoluta a tu proyecto (ajusta si tu usuario o carpeta cambia)
path = '/home/DCphone/phone_store'
if path not in sys.path:
    sys.path.append(path)

# Configura el entorno de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'phone_store.settings'

# Si usas virtualenv, PythonAnywhere lo activa automáticamente si lo configuras en el panel web
# Si necesitas activarlo manualmente, descomenta y ajusta:
# activate_this = '/home/DCphone/.virtualenvs/phone_store_env/bin/activate_this.py'
# with open(activate_this) as file_:
#     exec(file_.read(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 