import numpy as np

def load_3d_filter_from_file(path):
    """
    Faz a leitura de um filtro 3d em um arquivo de texto como:

    3 3 3

    a b c
    d e f
    g h i

    a b c
    d e f
    g h i

    a b c
    d e f
    g h i

    e retorna um np.array na formatado como

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
    
    # a primeira linha do arquivo tem informações sobre a quantidade de linhas, colunas e canais da mascara
    m, n, c = map(int, lines[0].split())

    aux = []
    matrix = []
    mask = []

    #itera pelas linhas colocando cada canal da mascara em uma matriz diferente
    for line in lines[1:]:
        if line == '':
            mask.append(matrix)
            matrix = []
            continue

        aux = [float(v) for v in line.split()]
        matrix.append(aux)
    
    if len(matrix) > 0:
        mask.append(matrix)

    pixel = []
    colum = []
    matrix = []

    #itera pelas matrizes obtidas anteriormente e coloca todas
    #as bandas em uma determinada coordenada em apenas um pixel
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
