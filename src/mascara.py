import numpy as np
from scipy import ndimage

#abaixo definimos nossos limiares de nuvens
LIMIAR_B11 = 0.02
#banda do SWIR (short-wave infrared), que é a banda do infravermelho de onda curta
#água limpa fica em valores muito menores, já as nuvens passam de 0.1

LIMIAR_B10 = 0.005
#banda B10 ou Cirrus, Ceú liimpo fica perto de 0.001, acima do nosso limiar são nuvens altas.


RAIO_ABERTURA = 1
#ao analizar as matrizes vamos ter raios de abertura, onde 1 faz uma cruz em uma matriz 3x3 por exemplo.
#logo a abertura que definimos aqui, apaga as manchas qeu não cabem o disco de raio 1.

AREA_PIXEL_KM2 = 0.02 * 0.02
#definimos y e x na hora de baixar as imagens como 20m x 20m, logo cada pixel = 0.02km x 0.02km = 0.0004km²

RAIO_MARGEM = 5
#aqui definimos o tamanho da margem em volta da nuvem (ou possível terra) ex: 5px = 100m

MIN_FRACAO_AGUA = 0.05
#Não é o caso do nosso dataset, mas... caso uma cena venha a ter menos de 5% de água
#a Cena não é corrigida

#tomamos esses dentro outros cuidados caso haja adicao de mais dados futuramente. dependedendo se o feedback do professor achar que temos o suficiente.


def disco(raio):
    #aqui definimos o que vai ser o nosso disco (estrutura mofológica), no fim vai ser uma matriz de true e false
    #onde vamos aplicar um disco no meio, e apagamos o que não estiver no disco.
    y, x = np.ogrid[-raio:raio + 1, -raio:raio + 1]
    #y e x são basicamente a distância do cetrno do disco. raio a distancia max.
    return x ** 2 + y ** 2 <= raio ** 2


def mascara_nuvens(bandas):
    #aqui vamos usar nossos limiares de nuvem definidos la em cima, basicamente acima deles = é nuvem (true)
    return (bandas["B11"] > LIMIAR_B11) | (bandas["B10"] > LIMIAR_B10)

def abertura(mascara, raio=RAIO_ABERTURA):
    if raio == 0:
        return mascara
    return ndimage.binary_opening(mascara, structure=disco(raio))
    #Essa parte talvez seja mais difícil de explicar, mas aqui, basicamente os pixels soltos depois da erosão, são apagados
    #já os do disco permanecem para a dilatacao. no caso os que cabem a mancha (min de raio = 1).
    

def mascara_terra(bandas, nuvem): #opcional para nosso dataset, mas pode ser necessário para futuro.
    #fazemos o cálculo do NDWI (Normalized Difference Water Index) para identificar a água. (verde -NIR)/(verde + NIR)
    #fazemos isso pq na água o B03 (nosso verde) reflete mais que o NIR, então NWDI positivo = água, negativo = terra.
    ndwi = (bandas["B03"] - bandas["B08"]) / (bandas["B03"] + bandas["B08"] + 1e-6) #a última parte é para evitar divisão por zero, caso não haja dado.
    return (ndwi < 0) & ~nuvem 
    #o ~ é um não, para oq é nuvem n virar terra.
    
    
def mascara_margem(nuvem, terra, raio=RAIO_MARGEM):
    #aqui vamos usar nosso limiar de margem, onde crescemos 5px para todos os lados.
    crescida = ndimage.binary_dilation(nuvem | terra, structure=disco(raio))
    #basicamente juntamos tudo que vamos tirar (tudo qu não é água)
    return crescida & ~nuvem & ~terra #novamente o ~ para n misturar.


def descrever_nuvens(nuvem):
    #aqui uma das coisas que aprendemos na M2, componentes conexos: cada nuvem vai receber um número (Rótulo).
    vizinhanca_8 = np.ones((3, 3)) #8 pq em uma 3x3 (nosso menor disco) o centro tem 8 vizinhos.
    #rotulos vai ser uma matriz do mesmo tamanho, onde 0 vai ser o fundo e 1,2,3 ... cada nuvem.
    rotulos, quantidade = ndimage.label(nuvem, structure=vizinhanca_8)
    areas = np.bincount(rotulos.ravel()) [1:] * AREA_PIXEL_KM2
    return {
        "quantidade": quantidade,
        "area_total_km2": areas.sum(),
        "maior_area_km2": areas.max() if quantidade > 0 else 0,
    }
    

def calcular_mascara(bandas, tem_dado, raio_abertura=RAIO_ABERTURA):
    nuvem = abertura(mascara_nuvens(bandas), raio_abertura) & tem_dado
    terra = mascara_terra(bandas, nuvem) & tem_dado
    margem = mascara_margem(nuvem, terra) & tem_dado
    agua = tem_dado & ~nuvem & ~terra & ~margem
    #chamamos na ordem, e cada uma usa os dados da anterior, e no final temos a máscara de água.
    return {"nuvem": nuvem, "terra": terra, "margem": margem, "agua": agua}


def agua_suficiente(agua, tem_dado):
    return (agua.sum() / tem_dado.sum()) >= MIN_FRACAO_AGUA
    #testa min de água.
    


if __name__ == "__main__":
    #teste 4 mascaras aplicadas.
    
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    from figuras import cor_verdadeira
    from leitura import PASTA_ENTRADA, ler_cena
    #sobre os imports aqui dentro, é para usar somento no teste não toda vez que usar o mascara.py.
    
    #aqui abaixo podemos mudar a AOI e a data para testar em outras cenas.
    pasta = PASTA_ENTRADA / "AOI_1_Florianopolis" / "Florianopolis_L1C_2026_06_16"
    bandas, tem_dado = ler_cena(pasta)
    
    #no teste feremos sem e com abertura pra ver o impacto da abertura na mascara de nuvens.
    for raio in (0, RAIO_ABERTURA):
        classes =  calcular_mascara(bandas, tem_dado, raio_abertura=raio)
        
        nuvens = descrever_nuvens(classes["nuvem"])
        print(f"Abertura com raio {raio}:")
        for nome, matriz in classes.items():
            print(f"  {nome:6s} {100 * matriz[tem_dado].mean():5.1f}% dos pixels com dado")
        print(f"  nuvens: {nuvens['quantidade']} nuvens, área total {nuvens['area_total_km2']:.1f} km², "f"maior {nuvens['maior_area_km2']:.1f} km²")
        print(" corrigir a cena?", "sim" if agua_suficiente(classes["agua"], tem_dado) else "não")
    
        
    classes = calcular_mascara(bandas, tem_dado)
    mapa = np.zeros(tem_dado.shape) #0 = sem dado.
    mapa[classes["agua"]] = 1
    mapa[classes["margem"]] = 2
    mapa[classes["terra"]] = 3
    mapa[classes["nuvem"]] = 4
    cores = ListedColormap(["white", "navy", "orange", "green", "lightgray"])
    
    
    fig, eixos = plt.subplots(1, 2, figsize=(12, 5))
    eixos[0].imshow(cor_verdadeira(bandas, tem_dado))
    eixos[0].set_title("Cor verdadeira (L1C)")
    
    eixos[1].imshow(mapa, cmap=cores, vmin=0, vmax=4, interpolation="nearest")
    eixos[1].set_title("Azul: água | Laranja: margem | Verde: terra | Cinza: nuvem")
    
    for eixo in eixos:
        eixo.axis("off")
    plt.show()
