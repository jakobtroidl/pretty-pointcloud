import octarine as oc
import pygfx as gfx
import numpy as np

path = "./data/example2.npy"
points = np.load(path)


v = oc.Viewer()

# iterate over all points (N, 3)
for i in range(points.shape[0]):

    print("add sphere", i)

    # Make a simple cube
    sphere = gfx.Mesh(
        gfx.sphere_geometry(),
        gfx.MeshPhongMaterial(color="#336699"),
    )

    sphere.position = points[i]

    # Add to viewer
    v.add(sphere)

v.show(start_loop=True)