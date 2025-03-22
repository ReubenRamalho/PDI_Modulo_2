# correlation.py
"""
Module that implements:
- 2D correlation (without padding)
- Version with offset, stride, and ReLU (item 2)
- Function to apply correlation to all channels (R, G, B)
"""

import numpy as np

def corretlated_3d_mask(mask, image):
    imagem = np.array(image)
    m, n, qutd_chanels_maks = mask.shape
    qutd_chanels_image = imagem.shape[2]
    
    if qutd_chanels_maks != qutd_chanels_image:
        print(f'The image has {qutd_chanels_image} channels and the mask has {qutd_chanels_maks}')
        return None
    
    pivo = (int(m - 1 if m % 2 == 0 else (m-1)/2),
            int(n - 1 if m % 2 == 0 else (n-1)/2))
    
    init_y, init_x = pivo
    
    final_y = (imagem.shape[0] - 1) - ((m-1) - pivo[0])
    final_x = (imagem.shape[1] - 1) - ((n-1) - pivo[1])
    
    final_array = np.empty_like(imagem, dtype=np.int32)
    pixel_value = 0
    
    for y in range(pivo[0], final_y):
        for x in range(pivo[1], final_x):
            cut_m = list(range(y - m - 1, y + 1)) if m % 2 == 0 else list(range(int(y - (m-1)/2), int(y + (m-1)/2 + 1)))
            cut_n = list(range(x - n - 1, x + 1)) if n % 2 == 0 else list(range(int(x - (n-1)/2), int(x + (n-1)/2 + 1)))

            cut = imagem[np.ix_(cut_m, cut_n, list(range(qutd_chanels_image)))] 
                
            pixel_value = 0
            for i in range(m):
                for j in range(n):
                    for c in range(qutd_chanels_maks):
                        pixel_value += cut[i][j][c] * mask[i][j][c]

            for c in range(qutd_chanels_maks):
                final_array[y][x][c] = pixel_value
                #print(pixel_value, final_array[y][x][c])
            
    return final_array  

