import os
import shutil

# Correct paths
source_dir = r"C:\Users\HP\.gemini\antigravity\brain\0f96b094-f1f3-4732-aa31-742716f7768b"
target_dir = r"d:\404-CarService\static\images\services"

if not os.path.exists(target_dir):
    os.makedirs(target_dir, exist_ok=True)
    print(f"Created directory: {target_dir}")

files_to_copy = {
    "basic_exterior_wash_service_1773814012338.png": "basic_wash.png",
    "elite_interior_detail_service_1773814176652.png": "elite_interior.png",
    "showroom_wax_shine_service_1773814199385.png": "showroom_wax.png",
    "nano_ceramic_shield_service_1773814238389.png": "nano_ceramic.png",
    "wheel_tire_refurb_service_1773814272347.png" : "wheel_refurb.png",
    "ceramic_coating_ultra_service_1773814461700.png" : "ceramic_coating.png"
}

for src, dst in files_to_copy.items():
    src_path = os.path.join(source_dir, src)
    dst_path = os.path.join(target_dir, dst)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"Copied: {src} -> {dst}")
    else:
        print(f"Source NOT FOUND: {src}")
