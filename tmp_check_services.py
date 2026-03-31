import os
import django
import sys

# Setup Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_wash_main.settings') # need to confirm settings module
django.setup()

from services.models import Services

services = Services.objects.all()
for s in services:
    print(f"ID: {s.id}, Name: {s.name if hasattr(s, 'name') else s.service_name}")
