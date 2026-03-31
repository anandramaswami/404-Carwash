import os
import django
import sys

# Setup Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_wash_main.settings')
django.setup()

from services.models import Services

# Mapping images to services
mapping = {
    "Basic Exterior Wash": "/static/images/services/basic_wash.png",
    "Elite Interior Detail": "/static/images/services/elite_interior.png",
    "Showroom Wax Shine": "/static/images/services/showroom_wax.png",
    "Nano Ceramic Shield": "/static/images/services/nano_ceramic.png",
    "Wheel & Tire Refurb": "/static/images/services/wheel_refurb.png"
}

# Update existing
for name, url in mapping.items():
    Services.objects.filter(service_name=name).update(image_url=url)

# Add new service if not exists
if not Services.objects.filter(service_name="Ceramic Coating").exists():
    Services.objects.create(
        service_id=f"S-{Services.objects.count() + 1}",
        service_name="Ceramic Coating",
        description="Premium ultra-durable ceramic coating for long-lasting protection and high gloss showroom finish.",
        price=15000.00,
        duration_minutes="240",
        image_url="/static/images/services/ceramic_coating.png"
    )
else:
    Services.objects.filter(service_name="Ceramic Coating").update(image_url="/static/images/services/ceramic_coating.png")

print("Database updated with services and images.")
