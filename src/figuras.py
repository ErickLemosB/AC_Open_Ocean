from leitura import ler_cena, listar_cenas , RAIZ

import matplotlib.pyplot as plt
import numpy as np

ESCALA_MAX = 0.4 #no site da copernicus o ponto branco é x2,5 que é o mesmo que dividir por 0.4 (nossa constante)
PASTA_SAIDA = RAIZ / "images" / "results" / "true_color_outputs"

def cor_verdadeira(bandas, tem_dado):
    #Aqui montamos a imagem com os seguintes parâmetros: as 3 Bandas (RGB, que vão ter linha e coluna),
    #exemplo de como funcionaria: todo pixel a baixo de 0.4 seria pixel de água, ou seja os pixels não-brancos
    #caso o pixel seja de nuvem por exemplo, ao ser dividido pela nosa constante, ele vai sempre sair como 1 ou maior
    rgb = np.dstack([bandas["B04"], bandas["B03"], bandas["B02"]]) #vermelhor, verde e azul nosso RGB
    rgb = np.clip(rgb / ESCALA_MAX, 0, 1) #zero e um estão aqui para cortes, abaixo de 0 vira 0 e acima de 1 vira 1
    return np.dstack([rgb, tem_dado]) #aqui também é passado o datamask, onde verificamos a opacidade, para evitar que um pixel escuro se entenda como água escura.




if __name__ == "__main__":
    #teste 3: Geracao de imagens para todos os pares que temos (true color no caso)
    for cena in listar_cenas():
        bandas_l1c, tem_dado = ler_cena(cena["pasta_l1c"])
        bandas_l2a, _ = ler_cena(cena["pasta_l2a"])
        
        fig, eixos = plt.subplots(1, 2, figsize=(12, 6)) #aqui definimos a criacao das figuras, onde vão ter duas colunas uma para L1C e a outra para L2A. 12x5 polegadas.
        eixos[0].imshow(cor_verdadeira(bandas_l1c, tem_dado)) 
        eixos[0].set_title("L1C (TOA)")
        eixos[1].imshow(cor_verdadeira(bandas_l2a, tem_dado))
        eixos[1].set_title("L2A (BOA - Sen2Cor)")
        for eixo in eixos:
            eixo.axis("off") #serve apenas para tirar os números para ficar mais limpo
        fig.suptitle(f"{cena['aoi']} {cena['data']} - cor verdadeira, escala fixa de 0 a 0.4")
        
        saida = PASTA_SAIDA / f"{cena['aoi']}_{cena['data']}_true_color.png"
        fig.savefig(saida, dpi=150, bbox_inches="tight") #bbox serve para cortar as bordas.
        plt.close(fig) #da um close na figura salva para salvar memória.
        print("figura salva em", saida.relative_to(RAIZ))
