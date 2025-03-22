# image_utils.py
"""
Module responsible for reading and writing images (R, G, B) using Pillow (PIL).
Also contains auxiliary functions for channel manipulation and normalization.
"""

from PIL import Image
import numpy as np


def abs_and_expand_hist(image):
    image = np.abs(image)
    
    min_value = image.min()  # Chama o método min() para obter o valor mínimo
    max_value = image.max()  # Chama o método max() para obter o valor máximo
    
    image = ((image - min_value) / (max_value - min_value)) * 255
    
    return image.astype(np.uint8)
