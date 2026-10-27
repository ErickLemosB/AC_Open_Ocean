from pathlib import Path
import numpy as np
import rasterio

RAIZ = Path(__file__).resolve().parent.parent
PASTA_ENTRADA = RAIZ / "images" / "input"



def listar_cenas():
    #funcao que vai encontrar os pares de dados que temos (L1C e L2A) nas pastas de entrada. 1 por AOI.
    cenas = []
    for pasta_l1c in sorted(PASTA_ENTRADA).glob("AOI_*/*_L1C_*"):
        cenas.append({
            #Ao montar o dataset, seguimos um padrão de formatacao de nome para poder ter esse tipo de controle depois.
            "aoi": pasta_l1c.parent.name,              # "AOI_1_Florianopolis"
            "data": pasta_l1c.name.split("_L1C_")[1],  # "2026_06_16"
            "pasta_l1c": pasta_l1c,
            "pasta_l2a": pasta_l1c.with_name(pasta_l1c.name.replace("_L1C_", "_L2A_")),
        })
    return cenas

def ler_banda(caminho):
    #vai ler nosso TIFFs e devolver reflectância(0 ou 1) e dados(bolean se tem ou n os dados).
    with rasterio.open(caminho) as arquivo:
        reflectancia = arquivo.read(1)
        tem_dado = arquivo.read(2) == 1
    return reflectancia, tem_dado

def ler_cena(pasta):
    #agora que temos um leitor de bandas,  podemos construir o leitor de cenas, que vai ler todas as bandas de uma pasta de cena.
    arquivos = sorted(Path(pasta).glob("*.tiff"))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum TIFF em {pasta}")
    
    bandas = {}
    mascaras = []
    for caminho in arquivos:
        nome_banda = caminho.name.split("_")[-2]  #Para pegar o nome que importa, indice -2. (EX: B02, porque splitamos com _)
        reflectancia, tem_dado = ler_banda(caminho)
        bandas[nome_banda] = reflectancia
        mascaras.append(tem_dado)
    return bandas, np.all(mascaras, axis=0)

if __name__ == "__main__":
    # Teste 1: uma cena em detalhe.
    pasta_aoi = PASTA_ENTRADA / "AOI_1_Florianopolis"
    bandas_l1c, tem_dado = ler_cena(pasta_aoi / "Florianopolis_L1C_2026_06_16")
    bandas_l2a, _ = ler_cena(pasta_aoi / "Florianopolis_L2A_2026_06_16")
    print(f"Florianopolis 2026_06_16: shape {tem_dado.shape}, {100 * tem_dado.mean():.1f}% com dado")
    print("Banda  L1C mín   L1C máx   L2A mín  L2A máx   (pixels com dados válidos)")
    for nome in bandas_l1c:
        l1c = bandas_l1c[nome][tem_dado]
        linha = f"{nome:5s} {l1c.min():8.4f} {l1c.max():8.4f}"
        if nome in bandas_l2a:  #TIFFs de L2A n contém B10.
            l2a = bandas_l2a[nome][tem_dado]
            linha += f"  {l2a.min():8.4f} {l2a.max():8.4f}"
        print(linha)
