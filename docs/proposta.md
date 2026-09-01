**Projeto:** Correção atmosférica (AC) de imagens de sensoriamento remoto para áreas de oceano aberto

**1. Problema:** Imagens de satélites ou imagens de sensoriamento remoto (SR) capturam, no topo da atmosfera (TOA), sinais provenientes da superfície, que se misturam com sinais introduzidos pela atmosfera (espalhamento e a absorção causados por aerossóis e gases) e essa mistura influencia o que se observa da TOA com o que realmente tem na superfície, ou base da atmosfera (BOA). Sobre áreas de oceano aberto, o problema do espalhamento e absorção é mais severo, e dificulta o estudo e quantificação dos dados observados, pois a radiância capturada pelo sensor tem cerca de 90% de origem da atmosfera, e não da água em si. Logo, para extrair informações mais confiáveis, é necessário fazer essa correção atmosférica.

O projeto envolve processamento de imagens porque no processo a ser desenvolvido se prevê operações como:

1.1 Processamento pixel a pixel sobre matrizes multiespectrais (bandas capturadas pelo sensor do satélite, como a do infravermelho próximo).

1.2 Pré-processamento radiométrico (máscaras para tirar nuvens e etc)

1.3 Análise de resultados por comparação visual e quantitativa entre as imagens de entrada e saída.

**Situação Inicial:** Serão baixadas cenas de satélite que estão disponíveis publicamente em nível L1 (que refere-se a radiância e reflectância no topo da atmosfera TOA), sem a correção atmosférica aplicada, como na imagem de exemplo:

**ANTES:** <img width="1470" height="916" alt="2026-08-29-00_00_2026-08-29-23_59_Sentinel-2_L1C_True_color" src="https://github.com/user-attachments/assets/40bf9bec-95cf-49c8-a93a-4ae565d13725" />
Fig 1. Sentienl-2 LC1 true colors

**DEPOIS:**<img width="1470" height="916" alt="2026-08-29-00_00_2026-08-29-23_59_Sentinel-2_L2A_True_color (1)" src="https://github.com/user-attachments/assets/3b6ff96c-8700-46be-af48-746b5b7b8f11" />
Fig. 2 Sentinel-2 LA2 true colors

Nota: é importante notar que além da correção atmosférica, prevê=se uma máscara para remover as nuvens no "depois".

A informação a ser produzida é essa como mostrada na figura 2, uma estimativa da reflectância de água (Bottom of Atmosphere - BOA), concebida através da remoção da influência atmosférica presentes nas imagens como na figura 1 de nível L1.

**2. Contexto de aplicação:** A AC se mostra como uma etapa obrigatória de pré-processamento de dados em praticamente toda pesquisa e análise de sensoriamento remoto, independentemente da área de concentração da aplicação final. No caso deste projeto, escolhemos como foco o Oceano aberto, a ideia inicial seria corpos oceânicos no geral, porem tanto pelo tempo, quanto pela complexidade do problema, devido a algumas dificuldades encontradas para se utilizar apenas de um método para todos os corpos de água, como por exemplo áreas costeiras (que se demonstraram as mais desafiadoras por ter muita influência de outros elementos), decidimos diminuir os escopo do projeto apenas para Oceano aberto.

A correção da reflectância de água apoia um conjunto de aplicações, dentre elas:

2.1 Detecção de manchas de oléo e derramamentos.
   
2.2 Rastreamento de resíduos plásticos e outros detritos flutuantes.
   
2.3 Alertas precoce de floração de algas nocivas.
   
2.4 Suporte a gestão da pesca e mapear habitats marinhos. Dentre outros.

O monitoramento da "cor do oceano" é apenas um deles. 

Sobre o contexto de uso, ele é não comercial, o objetivo é conseguir reproduzir, nessa menor escala, esse pré-processamento.

**3. Objetivo:**  Desenvolver e avaliar um pipeline de correção atmosférica para imagens multiespectrais de satélite sobre águas oceânicas abertas, utilizando esse cenário como estudo de caso do problema geral de correção atmosférica em PDI, de modo a estimar a reflectância da água a partir de dados no topo da atmosfera e comparar os resultados com produtos oficiais de referência.

**Objetivos específicos:**

3.1 Adquirir e organizar uma database inicial de cenas do Sentinel-2 MSI, do nível L1C, sobre áreas de oceano aberto, através do Copernicus Data Space Ecosystem e/ou Google Earth Engine.

3.2 Pesquisar/investigar e testar o método clássico de correção atmosférica para águas case-1 (**black-pixel assumption**, Gordon e Wang, 1994), que usa de bandas do infra vermelho próximo (Short-Wave Infrared - SWIR), onde a reflectância da água é praticamente zero, para isolar e avaliar a influência da atmosfera.

3.3 Fazer uma avaliação sobre a diferença entre a imagem corrigida e alguma referência já existente. (comparação de resultado dos métodos)

3.4 Documentar as observações, incluindo falhas e acertos do método escolhido.

**4. Entrada e saída esperada:** 

**ENTRADA:** 
4.1 Imagem multiespectral Sentinel-2 MSI de nível L1C (ou seja, com a reflectância da TOA), com bandas do que se diz "visível" até o infravermelho próximo/SWIR (índice esse, que como outros, pode ser extraído do Google Earth Engine em formato de CSV, junto com as bandas e pixels da imagem)

4.2 Metadados de geometria, caso algum método torne necessário.

4.3 Máscaras para isolar nuvens/terra

**SAÍDA:**

4.4 Imagem de reflectância de água estimada (BOA), para áreas de oceano aberto da cena, pixel a pixel.

4.5 Comparação clara, visual e quantitativa (quando possível), entre a cena original (TOA) e a cena corrigida.

Fluxo planejado:

<img width="496" height="701" alt="Fluxo_Conceitual_PDI_M1_AC_Oceano_Aberto" src="https://github.com/user-attachments/assets/5d7d9fb3-8cb4-4887-b5fd-eb42926c2d19" />

(Método de mascaramento de nuvens ainda está em discussão, então as imagens de exemplo ainda possuem nuvens/terra)



**5. Imagens e dados:** Encontramos duas bases públicas de dados que fornecem imagens de satélite Sentinel-2 MSI, nível L1C (TOA):

5.1 Copernicus Data Space Ecosystem (ESA) — https://browser.dataspace.copernicus.eu/

5.2 Google Earth Engine (GEE) — https://code.earthengine.google.com/

Nessas bases as imagens podem ser baixadas em diferentes formatos e qualidades, incluindo matrizes em formato de CSV com as bandas e índices escolhidos (Google Earth Engine - GEE).

Exemplo de imagem em formato matricial: 

<img width="1569" height="792" alt="image" src="https://github.com/user-attachments/assets/22a38ef3-734f-46d3-a32d-3c4d13aac4e9" />

Podemos observar que na matriz extraída temos a coluna de indexes, as que começam com B que são as bandas dos sensores, logo ao lado os índices como NDWI (Normalized Difference Water Index - Índice de Água por Diferença Normalizada ), SWIR1 (Short-Wave Infrared 1 - Banda do infravermelho de ondas curtas 1), SWIR2 (Short-Wave Infrared 2 - Banda do infravermelho de ondas curtas 2).

**NDWI:** Se usa para identificar e analisar corpos d'água (geralmente utilizando bandas verdes e NIR(Near Infrared - Infravermelho próximo).

**SWIR1:** Corresponde a banda B11 do sentinel-2, que é principalmente mais sensível a umidade e composição da superfície.

**SWIR2:** Corresponde a banda B12 do Sentinel-2, se usa para analisar também a umidade, minerais e outras características da superfície. 

É possível notar que as bandas B11 e B12 são respectivamente correspondentes aos índices SWIR1 e SWIR2, onde foi mostrado apenas para ilustrar que são equivalentes. Também podemos observar que a latitude e longitude podem ser organizado no formato GeoJSON, essa informação é muito importante pois cada posição dessa representa a posição real de cada pixel da imagem. 

**Forma de obtenção:**  Os downloads dos dados podem ser feitos através dos links disponibilizados das plataformas: 
1 - https://browser.dataspace.copernicus.eu/ ESA/Copernicus 

2 - https://code.earthengine.google.com/ Google Earth Engine (GEE)

ou também por suas respectivas APIs. Porém, o mais interessante até agora é o GEE, pois por ele conseguimos personalizar mais a obtenção dos dados, pois ele suporta um editor de script onde podemos determinar várias características para fazer a extração dos dados.

Foi utilizada da inteligência artificial generativa para gerar um script para gerar nosso banco de dados inicial.

Script utilizado: https://github.com/ErickLemosB/AC_Open_Ocean/blob/main/src/scripts_GEE.js

O QUE ESTE SCRIPT FAZ:

   Pega 5 cenas Sentinel-2 (nível L1C, TOA — sem correção atmosférica) de
   cada uma das 4 regiões oceânicas abaixo, e para cada cena exporta:
     a) uma imagem "visível" (RGB, cor verdadeira) para o Google Drive;
     b) um CSV com B2, B3, B4, B8, NDWI, SWIR1, SWIR2, latitude,
        longitude e .geo, amostrados na grade de pixels da imagem.

Regiões oceânicas: 

South Atlantic — Santa Helena

Indian Ocean — Diego Garcia

North Atlantic — Faial, Açores

South Pacific — Ilha de Páscoa

   
**6. Pipeline preliminar:** 

**7. Arquitetura preliminar:**

**8. Estudo inicial e viabilidade:**

**9. Resultados ou experimentos preliminares:** Ainda não temos.

**10. Código e reprodutibilidade:** ainda não temos.

**11. Vídeo da M1:**
1. identificação da equipe e do projeto;
2. problema escolhido;
3. motivação e contexto;
4. objetivo;
5. exemplos das imagens;
6. entrada e saída esperadas;
7. pipeline proposto;
8. principais métodos inicialmente considerados;
9. organização do repositório;
10. experimentos ou protótipos já realizados, quando houver;
11. dificuldades ou incertezas encontradas;
12. próximos passos previstos para a M2.



