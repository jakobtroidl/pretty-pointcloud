import numpy as np

def write_ply(filename, vertices):
    """
    Write a PLY file from a numpy array of vertices.

    Args:
        filename (str): The name of the output PLY file.
        vertices (np.ndarray): A numpy array of shape (N, 3) where N is the
                               number of vertices, and each vertex has 3 values (x, y, z).
    """
    num_vertices = vertices.shape[0]
    
    # Create the header for the PLY file
    header = f"""ply
format ascii 1.0
element vertex {num_vertices}
property float x
property float y
property float z
end_header
"""
    # Write the header and vertices to the file
    with open(filename, 'w') as f:
        f.write(header)
        # Write the vertex data
        for vertex in vertices:
            f.write(f"{vertex[0]} {vertex[1]} {vertex[2]}\n")

# Example usage:

path = "./data/example2.npy"
points = np.load(path).astype(np.float32)

# Write the vertices to a PLY file
write_ply("output.ply", points)
