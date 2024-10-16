from wgpu.gui.auto import WgpuCanvas, run
import pygfx as gfx
import numpy as np


canvas = WgpuCanvas()
renderer = gfx.renderers.WgpuRenderer(canvas)
scene = gfx.Scene()
scene.add(gfx.Background.from_color("#FFFFFF"))

grid = gfx.Grid(
    None,
    gfx.GridMaterial(
        major_step=100,
        minor_step=10,
        thickness_space="world",
        major_thickness=2,
        minor_thickness=0.1,
        infinite=True,
    ),
    orientation="xz",
)
grid.local.y = -120
scene.add(grid)

# Create a bunch of points

path = "./data/example2.npy"
positions = np.load(path).astype(np.float32) * 50
n = positions.shape[0]
sizes = np.ones(n).astype(np.float32) * 0.1
colors = np.random.rand(n, 4).astype(np.float32)
geometry = gfx.Geometry(positions=positions, sizes=sizes, colors=colors)

material = gfx.PointsMaterial(
    color_mode="vertex", size_mode="vertex", size_space="world"
)
points = gfx.Points(geometry, material)
scene.add(points)

camera = gfx.PerspectiveCamera(50)
camera.show_object(scene)
controller = gfx.FlyController(camera, register_events=renderer)


if __name__ == "__main__":
    canvas.request_draw(lambda: renderer.render(scene, camera))
    run()