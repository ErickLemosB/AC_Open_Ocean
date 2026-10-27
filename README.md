# Atmospheric Correction Open Ocean 
Repositório referente a proposta da etapa M1 de PDI

**Proposta:** Correção atmosférica (AC) de imagens de sensoriamento remoto para áreas de oceano aberto

**Integrantes: Erick Lemos Barreto, Janine de Paula, Melissa Moreira de Oliveira**

**Link para apresentação M1:** https://youtu.be/p47_E4aDF2k

**Problema:** Imagens de satélites ou imagens de sensoriamento remoto (SR) capturam, no topo da atmosfera (TOA), sinais provenientes da superfície, que se misturam com sinais introduzidos pela atmosfera (espalhamento e a absorção causados por aerossóis e gases) e essa mistura influencia o que se observa da TOA com o que realmente tem na superfície, ou base da atmosfera (BOA). Sobre áreas de oceano aberto, o problema do espalhamento e absorção é mais severo, e dificulta o estudo e quantificação dos dados observados, pois a radiância capturada pelo sensor tem cerca de 90% de origem da atmosfera, e não da água em si. Logo, para extrair informações mais confiáveis, é necessário fazer essa correção atmosférica.

**Contexto:** A AC se mostra como uma etapa obrigatória de pré-processamento de dados em praticamente toda pesquisa e análise de sensoriamento remoto, independentemente da área de concentração da aplicação final. No caso deste projeto, escolhemos como foco o **Oceano aberto**, a ideia inicial seria corpos oceânicos no geral, porem tanto pelo tempo, quanto pela complexidade do problema, devido a algumas dificuldades encontradas para se utilizar apenas de um método para todos os corpos de água, como por exemplo áreas costeiras (que se demonstraram as mais desafiadoras por ter muita influência de outros elementos), decidimos diminuir os escopo do projeto apenas para Oceano aberto.  

**A correção da reflectância de água apoia um conjunto de aplicações, dentre elas:**

1. Detecção de manchas de oléo e derramamentos.
2. Rastreamento de resíduos plásticos e outros detritos flutuantes.
3. Alertas precoce de floração de algas nocivas.
4. Suporte a gestão da pesca e mapear habitats marinhos.
Dentre outros.

O monitoramento da "cor do oceano" é apenas um deles.

**Objetivo:** Desenvolver e avaliar um pipeline de correção atmosférica para imagens multiespectrais de satélite sobre águas oceânicas abertas, utilizando esse cenário como estudo de caso do problema geral de correção atmosférica em PDI, de modo a estimar a reflectância da água a partir de dados no topo da atmosfera e comparar os resultados com produtos oficiais de referência.

**Resumo da solução prevista:** A atual solução proposta ainda está sobre análise, mas é previsto um pipeline que vai receber as imagens de satélite em nível L1(Radiância/reflectância da TOA) em regiões de oceano aberto e vai produzir como saída uma estimativa da reflectância da água (BOA), removendo a influência da atmosfera. A ideia inicial seria baseada no método clássico de correção atmosférica para águas Case-1 (Black-pixel assumption, Gordon & Wang, 1994), onde se usa bandas do infravermelho próximo, onde a reflectância da água é praticamente zero, ficando assim, mais destacado a influência atmosférica.

Exemplo de correção atmosférica em terra/região costeira: <img width="900" height="748" alt="Correccion-atmosférica-de-imágenes-Sentinel-2" src="https://github.com/user-attachments/assets/70372420-6f6b-41da-ad25-7242b311c70a" />

GIS & BEERS. Lo deberías saber sobre las imágenes Sentinel-2. [S. l.], [s. d.]. Disponível em: https://www.gisandbeers.com/lo-deberias-saber-imagenes-sentinel-2/. Acesso em: 31 ago. 2026.


**Database:** Encontramos duas databases públicas para uso, que utilizam imagens do satélite Sentinel-2 MS1, no nível L1C (reflectância da TOA). Porém, só vamos utilizar a do copernicus, por ser 100% gratuita.
1. https://browser.dataspace.copernicus.eu/ ESA/Copernicus (A que vamos usar)
2. https://code.earthengine.google.com/ Google Earth Engine (GEE)

Imagem exemplo: <img width="1470" height="917" alt="2026-08-24-00_00_2026-08-24-23_59_Sentinel-2_L1C_True_color" src="https://github.com/user-attachments/assets/63f9507a-7531-42b0-bb30-1c85f31bb142" />

**Especificações dos dados:**

**1. Formato dos dados:** As imagens baixadas do Copernicus virão em formato de TIFF, pois vem com a reflectância física (0-1) já pronta.

**2. Resolução da imagem:** Resolução custom para 20m, onde virão com a resolução por volta de 2100 x 1416 px (dependendo da seleção). Essa escolha se deve por que as bandas B8A, B11 e B12 são nativas de 20m, e são as bandas mais importantes pare o projeto (NIR e SWIR).

**3. Dados de posição:** Sobre o sistema de coordenadas, vai ser UTM da zona do tile escolhido, para facilitar alguns cálculos e entendimento, pois ela representa posições geográficas em metros.

**4. Bandas extraídas:** 

| Banda            | λ (nm)          | Motivos/descrição                                                                    |
| ---------------- | --------------- | ------------------------------------------------------------------------------------ |
| B01              | 443             | Banda aerossol/costeira, essencial para cor do oceano e mais sensível à atmosfera    |
| B02, B03, B04    | 490 / 560 / 665 | Visível, onde está o sinal da água                                                   |
| B05              | 705             | Red-edge, útil para clorofila e floração de algas                                    |
| B06, B07         | 740 / 783       | B07 + B8A formam um par NIR                                                          |
| B08              | 842             | NIR largo, opcional se já tiverem B8A                                                |
| B8A              | 865             | NIR estreito, a banda clássica do black-pixel                                        |
| B11, B12         | 1610 / 2190     | Par SWIR. Sobre o oceano a água é de fato preta aqui; é a variante SWIR              |
| B10 (só L1C)     | 1375            | Cirrus, ótima para mascarar nuvens finas                                             |

**5. Montagem do Dataset:** para montar o Dataset, foram selecionadas 4 AOIs (Areas of Interest), de tamanho compatível com a resolução escolhida e em 3 datas diferentes do ano, em níveis L1C (TOA) e L2A(BOA) para ter mais dados em relação a posição do sol. Juntamente com a extração das bandas citadas, também foi extraído (através de scripts) 4 importantes variáveis que vão ser importantes para o pre-processamento dos dados, são esses: 

**5.1 Ângulo zenital solar**: Ângulo entre a direção do Sol e a vertical local

<img width="300" height="250" alt="image" src="https://github.com/user-attachments/assets/861bec02-e290-44ab-920a-1e00e20d87d8" />

**5.2 Ângulo azimutal solar**: Indica a direção horizontal de onde vem a luz solar

<img width="300" height="250" alt="image" src="https://github.com/user-attachments/assets/2ab15f99-16e2-400b-8dfe-45a72be2684f" />

**5.3 Ângulo zenital médio de observação**: Representa o ângulo médio entre a direção de observação do sensor e a vertical local.

<img width="300" height="250" alt="image" src="https://github.com/user-attachments/assets/2636808d-9c38-4a19-8b3d-3510698ad885" />

**5.4 Ângulo azimutal médio de observação**: Indica a direção horizontal média para a qual o sensor está apontado

<img width="300" height="250" alt="image" src="https://github.com/user-attachments/assets/f20ec394-a658-4579-9232-d4ab6f066207" />

Esses dados vão servir para a correção de Rayleigh (espalhamento de raios) que vem antes do black-pixel.

**Estado atual do projeto:** Já temos alguns códigos testando o início da nossa implementação, leitura das imagens, montagem de figura em cores verdadeiras e a implementação das mascaras já estão funcionais no projeto e já geraram resultado.

**Tecnologias previstas:** O projeto está sendo desenvolvido em Pyhton, aproveitando de bibliotecas já consolidadas de SR e PDI. É pretendido usar dados da copernicus, numpy para operações sobre as matrizes que contem as bandas, além de outras como matplotlib para fazer comparações, scipy para complementar o numpy. Podemos acompanhar as tecnologias em [requirements.txt](https://github.com/ErickLemosB/AC_Open_Ocean/tree/main/requirements.txt)
