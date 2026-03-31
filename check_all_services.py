import os
import django
import sys

# Setup Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_wash_main.settings')
django.setup()

from services.models import Services

services = Services.objects.all()
print(f"Count: {services.count()}")
for s in services:
    print(f"NAME: {s.service_name}")
