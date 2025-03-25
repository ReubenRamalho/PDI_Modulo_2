import numpy as np

def corretlated_3d_mask(mask, image):

    # converte a imagem em um np.array
    imagem = np.array(image)

    # altura, largura e quantidade de canais da mascara
    m, n, qutd_chanels_maks = mask.shape

    # quantidade de canais da imagem
    qutd_chanels_image = imagem.shape[2]
    
    #verifica se a quantidade de canais da mascara é igual a quantidade de canais da imagem
    if qutd_chanels_maks != qutd_chanels_image:
        print(f'The image has {qutd_chanels_image} channels and the mask has {qutd_chanels_maks}')
        return None
    
    # pivo escolhido como o elemento mais acima e mais a esquerda da imagem 

    # final_x e final_y são os limites da imagem onde a mascara pode ser aplicada  
    final_y = (imagem.shape[0] - 1) - (m - 1)
    final_x = (imagem.shape[1] - 1) - (n - 1)
    
    # array final que será retornado nas mesmas dimensões da imagem
    final_array = np.empty_like(imagem, dtype=np.int32)
    pixel_value = 0
    
    # itera pelas linhas da imagem
    # a estratégia foi realizar um corte na imagem do tamanho da mascara e iterar pelo corte 
    for y in range(final_y):
        cut_m = list(range(y, y + m)) # coordenadas do corte vertical da imagem

        # itera pelas colunas da imagem
        for x in range(final_x):
            cut_n = list(range(x, x + n)) #coordenadas de corte horizontal da imagem

            # corte da imagem
            cut = imagem[np.ix_(cut_m, cut_n, list(range(qutd_chanels_image)))] 

            pixel_value = 0 # variável auxiliar para o produto interno de Frobenius

            #iterando pela mascara e pelo corte feito na imagem
            for i in range(m):#itera pelas linhas da mascara e da imagem
                for j in range(n): #itera pelas colunas da mascara e da imagem
                    for c in range(qutd_chanels_maks): #itera pelos canais da mascara e da imagem
                        pixel_value += cut[i][j][c] * mask[i][j][c] #produto interno de Frobenius

            #itera pelos canais da imagem de saída
            for c in range(qutd_chanels_maks):
                #coloca o resultado do produto interno de Frobenius em cada um dos canais
                # equivalentes ao pixel da imagem de saída de saída
                final_array[y][x][c] = pixel_value
            
    return final_array  

