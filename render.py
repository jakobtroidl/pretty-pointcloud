import bpy
import numpy as np
import random
import os

# Generate random colors for each point in the point cloud
def random_color():
    return (random.random(), random.random(), random.random(), 1.0)

# Function to create material for each point with a random color
def create_random_material():
    mat = bpy.data.materials.new(name="RandomColorMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    color = random_color()
    bsdf.inputs['Base Color'].default_value = color
    return mat

# Function to create a point cloud as a collection of spheres
def create_point_cloud(points, point_size=0.05):
    # Create a new collection for the point cloud
    collection = bpy.data.collections.new("PointCloud")
    bpy.context.scene.collection.children.link(collection)

    # Create a sphere for each point
    for idx, point in enumerate(points):
        # Create a sphere mesh
        bpy.ops.mesh.primitive_uv_sphere_add(radius=point_size, location=point)
        sphere = bpy.context.object

        # Assign a random color material to the sphere
        mat = create_random_material()
        if sphere.data.materials:
            sphere.data.materials[0] = mat
        else:
            sphere.data.materials.append(mat)

        # Move the sphere into the point cloud collection
        bpy.ops.collection.objects_remove_all()
        collection.objects.link(sphere)

# Set up lighting and shadows
def setup_lighting():
    # Create a sun lamp
    bpy.ops.object.light_add(type='SUN', radius=1, location=(10, 10, 10))
    sun = bpy.context.object
    sun.data.energy = 5
    sun.data.use_shadow = True

    # Optionally, create additional lighting for better shadows
    bpy.ops.object.light_add(type='AREA', location=(-10, -10, 10))
    area_light = bpy.context.object
    area_light.data.size = 5
    area_light.data.energy = 1000
    area_light.data.use_shadow = True

# Set up the camera
def setup_camera():
    # Create a camera
    bpy.ops.object.camera_add(location=(5, -5, 5), rotation=(1.1, 0, 0.7))
    camera = bpy.context.object
    bpy.context.scene.camera = camera

# Render the scene
def render_scene(output_path):
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)

print("Rendering point cloud...")
print("pwd: ", os.getcwd())

path = "./data/example.npy"

# Example point cloud data (replace this with your numpy array)
point_cloud_data = np.load(path)

# Convert numpy array to list of tuples for Blender
points = [tuple(point) for point in point_cloud_data]

# Create the point cloud
create_point_cloud(points)

# Set up the lighting, camera, and render the scene
setup_lighting()
setup_camera()

# Render and save the image
output_file_path = "/Users/jakobtroidl/Desktop/point_cloud_render.png"  # Change to your preferred path
render_scene(output_file_path)

print(f"Render saved to {output_file_path}")
