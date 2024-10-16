import numpy as np
from vispy import app, scene

# Create a canvas
canvas = scene.SceneCanvas(keys='interactive', show=True)

# Create a 3D view
view = canvas.central_widget.add_view()

# Generate random point cloud data (replace with your actual point cloud)
path = "./data/example2.npy"
points = np.load(path).astype(np.float32) * 50

# Create a scatter plot for the point cloud
scatter = scene.visuals.Markers()
scatter.set_data(points, edge_color=None, face_color=(1, 1, 1, 1), size=5)

# Add the scatter plot to the view
view.add(scatter)

# Enable lighting (for shadows)
view.camera = scene.cameras.TurntableCamera(fov=45)
view.camera.set_range(x=(-1, 1), y=(-1, 1), z=(-1, 1))

# Run the application
if __name__ == '__main__':
    app.run()
