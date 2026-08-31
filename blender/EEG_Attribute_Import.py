import bpy
import numpy as np
import os
from bpy.app.handlers import persistent

PROJECT_DIR = os.path.dirname(os.path.dirname(bpy.data.filepath))

bands = ['delta', 'theta', 'alpha', 'beta', 'gamma']
band_data = {}
for band in bands:
    band_data[band] = np.load(f"{PROJECT_DIR}/Data/processed/EEG/{band}_power.npy")

nearest_electrodes = np.load(f"{PROJECT_DIR}/Data/processed/EEG/vertex_nearest_electrodes.npy")
weights = np.load(f"{PROJECT_DIR}/Data/processed/EEG/vertex_weights.npy")

lh_obj = bpy.data.objects["lh_brain"]
rh_obj = bpy.data.objects["rh_brain"]
lh_count = len(lh_obj.data.vertices)

for obj in [lh_obj, rh_obj]:
    for band in bands:
        if band not in obj.data.attributes:
            obj.data.attributes.new(name=band, type="FLOAT", domain="POINT")

@persistent
def update_eeg(scene):
    frame = scene.frame_current % band_data['delta'].shape[1]
    for band in bands:
        power_at_electrodes = band_data[band][:, frame]
        vertex_power = (power_at_electrodes[nearest_electrodes] * weights).sum(axis=1)
        lh_obj.data.attributes[band].data.foreach_set("value", vertex_power[:lh_count].astype(np.float32))
        rh_obj.data.attributes[band].data.foreach_set("value", vertex_power[lh_count:].astype(np.float32))

# Remove ALL existing update_eeg handlers safely
bpy.app.handlers.frame_change_post[:] = [
    h for h in bpy.app.handlers.frame_change_post
    if h.__name__ != "update_eeg"
]

bpy.app.handlers.frame_change_post.append(update_eeg)
n = sum(1 for h in bpy.app.handlers.frame_change_post if h.__name__ == "update_eeg")
print(f"EEG handler registered! (active handlers: {n})")
