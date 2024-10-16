import bpy
import numpy as np
from time import time
from mathutils import Vector


# Clear existing mesh data
def clear_scene():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

# Create a UV Sphere at a given location with a specific radius
def create_sphere(location, radius=0.1):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location, segments=16, ring_count=8)

# Add a camera to the scene
def setup_camera(location=(0, -10, 5), rotation=(1.1, 0, 1.57)):
    bpy.ops.object.camera_add(location=location, rotation=rotation)
    camera = bpy.context.object
    bpy.context.scene.camera = camera

# Add a light source to the scene
def setup_light(location=(5, -5, 10), energy=1000):
    bpy.ops.object.light_add(type='POINT', location=location)
    light = bpy.context.object
    light.data.energy = energy

# Set up rendering parameters
def setup_render(filepath='rendered_image.png', resolution=(1920, 1080)):
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = filepath
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]
    scene.render.film_transparent = True

# Main function to generate spheres
def generate_spheres(points, radius=0.1):
    t = time()
    C = bpy.context

    scale = 25

    # Open textfile to numpy array and scale
    pointcloudfilepath = './data/point_data.txt'
    with open( pointcloudfilepath ) as fh:
        data = np.loadtxt( fh ) * scale

    print( f'vertcount = {len(data)}')

    # Create and arrange mesh data
    verts = [ Vector( data[i,:3] ) for i in range(data.shape[0]) ]
    m     = bpy.data.meshes.new('pc')
    m.from_pydata(verts, [], [])

    # Create mesh object and link to scene collection
    o = bpy.data.objects.new( 'pc', m )
    C.scene.collection.objects.link( o )

    # Add minimal icosphere
    bpy.ops.mesh.primitive_ico_sphere_add( subdivisions = 1, radius = 0.05 )
    isobj = bpy.data.objects[ C.object.name ]

    # Set instancing props
    for ob in [ isobj, o ]:
        ob.instance_type               = 'VERTS'
        ob.show_instancer_for_viewport = False
        ob.show_instancer_for_render   = False

    # Set instance parenting (parent icosphere to verts)
    o.select_set(True)
    C.view_layer.objects.active = o

    bpy.ops.object.parent_set( type = 'VERTEX', keep_transform = True )

    print( f'Total time = {time() - t} seconds' )


# Example of 4000 random points in N,3 format
# Replace this with your actual NumPy array
N = 1000
points = np.random.uniform(-5, 5, (N, 3))

# Call the function to generate spheres
generate_spheres(points)

# Set up the camera and light
setup_camera(location=(0, -20, 10), rotation=(1.1, 0, 1.57))  # Adjust camera position as needed
setup_light(location=(10, -10, 20), energy=1200)  # Adjust light source position and energy as needed


# reduce number of samples
bpy.context.scene.cycles.samples = 16

# Set up render settings
setup_render(filepath='./rendered_image.png', resolution=(400, 400))

# Render the scene
bpy.ops.render.render(write_still=True)
