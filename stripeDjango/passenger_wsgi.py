import os, sys
from django.core.wsgi import get_wsgi_application

site_user_root_dir = 'root/path'
sys.path.insert(0, os.path.join(site_user_root_dir, 'stripeDjango'))
sys.path.insert(1, os.path.join(site_user_root_dir, 'venv/lib/python3.6/site-packages'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stripeDjango.settings')

application = get_wsgi_application()