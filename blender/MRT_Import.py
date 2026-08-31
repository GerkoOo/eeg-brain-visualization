import bpy
import numpy as np
import os
PROJECT_DIR = os.path.dirname(os.path.dirname(bpy.data.filepath))

def create_brain_mesh(name, verts, faces):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    mesh.from_pydata(verts.tolist(), [], faces.tolist())
    mesh.update()
    return obj

# Remove old objects
for obj in bpy.data.objects:
    if obj.name in ["Brain", "lh_brain", "rh_brain"]:
        bpy.data.objects.remove(obj, do_unlink=True)
        
        

# Load pial surfaces
lh_verts = np.load(f"{PROJECT_DIR}/Data/processed/MRT/lh_pial.npy")
lh_faces = np.load(f"{PROJECT_DIR}/Data/processed/MRT/lh_faces.npy")
rh_verts = np.load(f"{PROJECT_DIR}/Data/processed/MRT/rh_pial.npy")
rh_faces = np.load(f"{PROJECT_DIR}/Data/processed/MRT/rh_faces.npy")

lh_obj = create_brain_mesh("lh_brain", lh_verts, lh_faces)
rh_obj = create_brain_mesh("rh_brain", rh_verts, rh_faces)

for obj in [lh_obj, rh_obj]:
    obj.rotation_euler[2] = -1.5708 * 2
    obj.location[2] = 0.91

for obj in [lh_obj, rh_obj]:
    obj.select_set(True)
    bpy.ops.object.shade_smooth()
    obj.select_set(False)

print("Done!")