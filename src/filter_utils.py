import numpy as np

def load_3d_filter_from_file(path):
    """
    Reads a 3D filter file and returns a NumPy array formatted as:
    
    np.array([
        [
            [a, a, a], [b, b, b], [c, c, c]
        ],
        [
            [d, d, d], [e, e, e], [f, f, f]
        ],
        [
            [g, g, g], [h, h, h], [i, i, i]
        ]
    ])
    """

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines()]  # Preserve empty lines
    # --- 1. Extract dimensions ---
    m, n, c = map(int, lines[0].split())  # First line defines matrix size
    
    linha = []
    matrix = []
    mask = []
    # --- 2. Read all slices ---
    for line in lines[1:]:
        if line == '':
            mask.append(matrix)
            matrix = []
            continue

        linha = [float(v) for v in line.split()]
        matrix.append(linha)
    
    if len(matrix) > 0:
        mask.append(matrix)

    pixel = []
    colum = []
    matrix = []

    for i in range(m):
        for j in range(n):
            for k in range(c):
                pixel.append(mask[k][i][j])
            colum.append(pixel)
            pixel = []
        matrix.append(colum)
        colum = []

    matrix = np.array(matrix)
    return matrix
