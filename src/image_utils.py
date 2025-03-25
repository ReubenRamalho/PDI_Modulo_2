from PIL import Image
import numpy as np


def abs_and_expand_hist(image):
    image = np.abs(image) # Transforma todos os valores da imagem em positivos
    
    min_value = image.min() #valor mínimo da imagem
    max_value = image.max() #valor máximo da imagem
    
    image = ((image - min_value) / (max_value - min_value)) * 255 #expande o histograma nomalizando os valores entre 0 e 255
    
    return image.astype(np.uint8) #retorna a imagem com os valores normalizados entre 0 e 255
