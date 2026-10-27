# M2 - Implementação parcial e análise técnica

Projeto: Correção atmosférica (AC) de imagens de sensoriamento remoto para áreas de oceano aberto

Integrantes: Erick Lemos Barreto, Janine de Paula, Melissa Moreira de Oliveira

Link para apresentação M2: **ADICIONAR O LINK AQUI**

---

## 1. Síntese do Problema

A nossa proposta aborda o problema da correção atmosférica (AC) em imagens de sensoriamento remoto, com foco específico em ambientes de oceano aberto. As imagens capturadas pelo sensor no Topo da Atmosfera (TOA, Nível L1C) agregam tanto a resposta radiométrica da superfície quanto os efeitos de espalhamento e absorção causados por gases e aerossóis. Em ecossistemas oceânicos abertos, essa distorção atmosférica se mostra particularmente severa, visto que aproximadamente 90% da radiância total registrada pelo sensor vem da atmosfera, o que compromete a confiabilidade de análises voltadas à cor da água. O objetivo central do projeto consiste no desenvolvimento e na avaliação de um pipeline computacional de processamento digital de imagens (PDI) para estimar a reflectância da água na Base da Atmosfera (BOA), a partir da aplicação de técnicas clássicas como o modelo de correção baseado na premissa do pixel escuro (black-pixel assumption, Gordon e Wang, 1994) com o auxílio de bandas do infravermelho próximo (NIR) e de ondas curtas (SWIR), além da correção do espalhamento de Rayleigh orientada por parâmetros de geometria solar e de visada. Metodologicamente, o estudo utiliza um conjunto de dados composto por cenas do satélite Sentinel-2 MSI obtidas por meio do Copernicus Data Space Ecosystem, estruturado em Áreas de Interesse (AOIs) representativas.

## 2. Objetivo atual

Na etapa M2, o enfoque recai sobre segmentação, morfologia e descrição de regiões. Nesse sentido, foi implementada a segmentação dos pixels de água, pré-requisito do método black-pixel, que opera sobre áreas livres de nuvens. A segmentação combina limiarização nas bandas B11 e B10, abertura morfológica, rotulagem de componentes conexos, detecção de terra por índice espectral (NDWI) e margem de segurança ao redor dos objetos excluídos. A correção de Rayleigh, o método black-pixel e a comparação com o L2A permanecem como etapas pendentes, previstas para a M3.

## 3. Resposta ao feedback 

PREENCHER

## 4. Evolução desde a M1;

PREENCHER

## 5. Dados utilizados
 
Foi utilizado uma base pública de dados que fornece imagens de satélite Sentinel-2 MSI, nível L1C (TOA) e nível L2A (BOA):https://browser.dataspace.copernicus.eu/

ou também por sua respectiva API.

Através do site da Copernicus, conseguimos montar nosso Dataset de 4 áreas de interesse distintas.

## 6. Protocolo experimental
 
| Teste | Dados | Procedimento | Critério de verificação |
| --- | --- | --- | --- |
| **1** (`leitura.py`) | Um par: Florianópolis, 2026_06_16 | Impressão do formato da imagem, da % de pixels com dado e do mínimo e do máximo de cada banda em L1C e L2A | Conferência visual dos valores. A ausência de B10 no L2A é esperada. |
| **2** (`leitura.py`) | Os 12 pares | Comparação do número de bandas, do formato da imagem e da % com dado, e verificação da igualdade da máscara de dados entre L1C e L2A (`np.array_equal`) | Resposta "sim" ou "não" por par. Concluiu-se que os pares são consistentes. |
| **3** (`figuras.py`) | Os 12 pares | Geração da imagem em cor verdadeira (B04, B03 e B02 divididas por 0,4 e limitadas a 0–1), com L1C e L2A lado a lado, salva em `images/results/true_color_outputs/` | Comparação visual com a cor verdadeira do site do Copernicus. |
| **4** (`mascara.py`) | Uma cena: Florianópolis, 2026_06_16, apenas L1C | Cálculo das máscaras de nuvem, terra, margem e água com abertura de raio 0 e de raio 1. Impressão da % por classe, do número de nuvens, da área total, da maior nuvem e da suficiência de água. Geração do mapa de classes. | Inspeção visual do mapa em relação à imagem. O grupo registrou que "condiz bem com a realidade". |
 
## 6.1. Parâmetros do Teste 4 (`mascara.py`)
 
| Parâmetro | Valor |
| --- | --- |
| `LIMIAR_B11` | 0,02 |
| `LIMIAR_B10` | 0,005 |
| `RAIO_ABERTURA` | 1 (comparado com 0) |
| `RAIO_MARGEM` | 5 px (100 m) |
| `MIN_FRACAO_AGUA` | 5% |
| `AREA_PIXEL_KM2` | 0,0004 km² |


 ## 7. Pipeline e Organização

O pipeline planejado compreende aquisição, pré-processamento, correção atmosférica, avaliação e visualização. Na M2, foram implementadas a leitura dos dados, a visualização em cor verdadeira e o pré-processamento, entendido como a segmentação dos pixels de água.

Fluxo implementado:
 
```
listar_cenas → ler_cena → calcular_mascara → descrever_nuvens
                              (nuvem → abertura → terra → margem → água)
```
 
## 7.1. Etapas implementadas
 
| Etapa | Função (arquivo) | Entrada | Saída | Parâmetros |
| --- | --- | --- | --- | --- |
| Descoberta de cenas | `listar_cenas`| `images/input/` | pares L1C/L2A por AOI e data | padrão de nome `AOI_*/*_L1C_*` |
| Leitura de bandas | `ler_banda`, `ler_cena` | pasta da cena (um `.tiff` por banda) | dicionário banda → reflectância; máscara de dados válidos | — |
| Cor verdadeira | `cor_verdadeira` | B04, B03, B02 e máscara de dados | imagem RGBA | escala fixa 0–0,4 |
| Detecção de nuvens | `mascara_nuvens` | B11, B10 | máscara booleana de nuvem | B11 > 0,02 ou B10 > 0,005 |
| Abertura morfológica | `abertura`, `disco` | máscara de nuvem | máscara sem detecções menores que o elemento estruturante | disco de raio 1 |
| Detecção de terra | `mascara_terra` | B03, B08, nuvem | máscara de terra | NDWI < 0, fora de nuvem |
| Margem de segurança | `mascara_margem` | nuvem, terra | anel ao redor de nuvem e terra | dilatação de 5 px (100 m) |
| Descrição de regiões | `descrever_nuvens` | máscara de nuvem | número de nuvens, área total e maior área (km²) | vizinhança-8; 0,0004 km²/pixel |
| Água utilizável | `calcular_mascara`, `agua_suficiente`| bandas e máscara de dados | máscara de água (com dado, sem nuvem, terra ou margem); decisão de corrigir a cena | mínimo de 5% de água |
 
 
## 7.2. Etapas pendentes
PREENCHER

 
## 8. Testes

| Teste | Objetivo | Resultado registrado |
|---|---|---|
| Teste 1 — leitura | Inspecionar um par de cenas e os valores das bandas | Leitura bem-sucedida; B10 ausente em L2A é esperado |
| Teste 2 — pares | Comparar shape e máscara de dados L1C/L2A | Dimensões e máscaras compatíveis nos pares testados |
| Teste 3 — RGB | Produzir cor verdadeira e comparar visualmente com o navegador Copernicus | Foram produzidas imagens RGB para as cenas |
| Teste 4 — máscara | Avaliar máscara de nuvens/terra/margem/água | Resultado visual considerado satisfatório |

### 8.1 Figuras de cor verdadeira

A seguir estão exemplos versionados do conjunto. A composição usa bandas B04, B03 e B02 e escala de exibição fixa. Estas figuras documentam cobertura e aparência visual, **não** resultados de correção atmosférica.

![AOI 1 — Florianópolis, 20 de janeiro de 2026, composição RGB L1C](../images/results/true_color_outputs/AOI_1_Florianopolis_2026_01_20_true_color.png)

*Figura 1 - Composição em cor verdadeira da AOI de Florianópolis em 20/01/2026. A imagem permite inspecionar a aparência geral da cena, mas não quantifica a reflectância da água nem demonstra remoção do caminho atmosférico.*

![AOI 2 — Canadá, 14 de maio de 2026, composição RGB L1C](../images/results/true_color_outputs/AOI_2_Canada_2026_05_14_true_color.png)

*Figura 2 - Composição em cor verdadeira da AOI do Canadá em 14/05/2026. A mesma escala de visualização facilita comparação visual entre cenas; diferenças de brilho podem decorrer tanto da cena quanto das condições de aquisição e da transformação de exibição.*

![AOI 3 — Noruega, 17 de maio de 2026, composição RGB L1C](../images/results/true_color_outputs/AOI_3_Norway_2026_05_17_true_color.png)

*Figura 3 - Composição em cor verdadeira da AOI da Noruega em 17/05/2026. A figura serve como inspeção qualitativa e não permite, isoladamente, atribuir diferenças visuais a aerossóis ou estimar a qualidade da correção.*

![AOI 4 — China, 27 de junho de 2026, composição RGB L1C](../images/results/true_color_outputs/AOI_4_China_2026_06_27_true_color.png)

*Figura 4 - Composição em cor verdadeira da AOI da China em 27/06/2026. A presença de quatro áreas geográficas amplia a diversidade de cenas, mas três datas por área ainda são uma amostra limitada para generalização.*

## 9. Falhas, limitações e riscos;

PREENCHER

## 10. Plano de conclusão para a M3

PREENCHER

## 11. Contribuições dos integrantes 

PREENCHER

## 12. Referências 

PREENCHER

## 13. Declaração de uso de IA.
 1. Tipo usado: Claude code
 2. Para quais fins?: 
  2.1 Commit automático do Dataset (montado manualmente).
  2.2 Gerar material de estudo para melhor entendimento dos assuntos abordados.
  2.3 Gerar exemplos de código para melhor entendimento do desenvolvimento.
  2.4 Auxílio no desenvolvimento do código para eventuais dúvidas durante o processo.
  2.5 Gerar o molde base do código nos padrões solicitados.
(Nota: Ouve uso do copilot para automatizar a descricao de alguns commits pela praticidade)
