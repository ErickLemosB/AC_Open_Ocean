**Projeto:** Correção atmosférica (AC) de imagens de sensoriamento remoto para áreas de oceano aberto

**Integrantes: Erick Lemos Barreto, Janine de Paula, Melissa Moreira de Oliveira**

**Link para apresentação M1:** https://youtu.be/p47_E4aDF2k

**Link para apresentação M2:** https://youtu.be/hud27jPzctY

**1. Problema:** Imagens de satélites ou imagens de sensoriamento remoto (SR) capturam, no topo da atmosfera (TOA), sinais provenientes da superfície, que se misturam com sinais introduzidos pela atmosfera (espalhamento e a absorção causados por aerossóis e gases) e essa mistura influencia o que se observa da TOA com o que realmente tem na superfície, ou base da atmosfera (BOA). Sobre áreas de oceano aberto, o problema do espalhamento e absorção é mais severo, e dificulta o estudo e quantificação dos dados observados, pois a radiância capturada pelo sensor tem cerca de 90% de origem da atmosfera, e não da água em si. Logo, para extrair informações mais confiáveis, é necessário fazer essa correção atmosférica.

O projeto envolve processamento de imagens porque no processo a ser desenvolvido se prevê operações como:

1.1 Processamento pixel a pixel sobre matrizes multiespectrais (bandas capturadas pelo sensor do satélite, como a do infravermelho próximo).

1.2 Pré-processamento radiométrico (máscaras para tirar nuvens e etc)

1.3 Análise de resultados por comparação visual e quantitativa entre as imagens de entrada e saída.

**Situação Inicial:** Foram baixadas imagens (TIFF) de satélite que estão disponíveis publicamente em nível L1C (que refere-se a radiância e reflectância no topo da atmosfera TOA), sem a correção atmosférica aplicada, como na imagem de exemplo:

**ANTES:** <img width="1470" height="916" alt="2026-08-29-00_00_2026-08-29-23_59_Sentinel-2_L1C_True_color" src="https://github.com/user-attachments/assets/40bf9bec-95cf-49c8-a93a-4ae565d13725" />
Fig 1. Sentienl-2 LC1 true colors

e também foram baixadas as mesmas imagens, nos mesmos locais e data de nível L2A (BOA, depois da correção). Como na imagem exemplo:

**DEPOIS:**<img width="1470" height="916" alt="2026-08-29-00_00_2026-08-29-23_59_Sentinel-2_L2A_True_color (1)" src="https://github.com/user-attachments/assets/3b6ff96c-8700-46be-af48-746b5b7b8f11" />
Fig. 2 Sentinel-2 LA2 true colors

A informação a ser produzida é essa como mostrada na figura 2, uma estimativa da reflectância de água (Bottom of Atmosphere - BOA), concebida através da remoção da influência atmosférica presentes nas imagens como na figura 1 de nível L1C.

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

3.1 Adquirir e organizar uma database inicial de cenas do Sentinel-2 MSI, do nível L1C, sobre áreas de oceano aberto, através do Copernicus Data Space Ecosystem. (feito)

3.2 Pesquisar/investigar e testar o método clássico de correção atmosférica para águas case-1 (**black-pixel assumption**, Gordon e Wang, 1994), que usa de bandas do infra vermelho próximo (Short-Wave Infrared - SWIR), onde a reflectância da água é praticamente zero, para isolar e avaliar a influência da atmosfera.

3.3 Fazer uma avaliação sobre a diferença entre a imagem corrigida e alguma referência já existente. (comparação de resultado dos métodos)

3.4 Documentar as observações, incluindo falhas e acertos do método escolhido.

**4. Entrada e saída esperada:** 

**ENTRADA:** 
4.1 Imagem multiespectral Sentinel-2 MSI de nível L1C (ou seja, com a reflectância da TOA), com bandas do que se diz "visível" até o infravermelho próximo/SWIR (índice esse, que como outros, pode ser extraído do Google Earth Engine em formato de CSV, junto com as bandas e pixels da imagem)

4.2 Metadados de geometria.

4.3 Máscaras para isolar nuvens/terra.

**SAÍDA:**

4.4 Imagem de reflectância de água estimada (BOA), para áreas de oceano aberto da cena, pixel a pixel.

4.5 Comparação clara, visual e quantitativa (quando possível), entre a cena original (TOA) e a cena corrigida.

Fluxo planejado:

<img width="496" height="701" alt="Fluxo_Conceitual_PDI_M1_AC_Oceano_Aberto" src="https://github.com/user-attachments/assets/5d7d9fb3-8cb4-4887-b5fd-eb42926c2d19" />

(Método de mascaramento de nuvens ainda está em discussão, então as imagens de exemplo ainda possuem nuvens/terra)



**5. Imagens e dados:** Encontramos uma base pública de dados que fornece imagens de satélite Sentinel-2 MSI, nível L1C (TOA) e nível L2A (BOA):

1 - https://browser.dataspace.copernicus.eu/

ou também por sua respectiva API.

Através do site da Copernicus, conseguimos montar nosso Dataset de 4 áreas de interesse distintas.

**5.1 Critérios de obtenção dos dados**: **1. Formato dos dados:** As imagens baixadas do Copernicus virão em formato de TIFF, pois vem com a reflectância física (0-1) já pronta.

**5.2 Resolução da imagem:** Resolução custom para 20m, onde virão com a resolução por volta de 2100 x 1416 px (dependendo da seleção). Essa escolha se deve por que as bandas B8A, B11 e B12 são nativas de 20m, e são as bandas mais importantes pare o projeto (NIR e SWIR).

**5.3 Dados de posição:** Sobre o sistema de coordenadas, vai ser UTM da zona do tile escolhido, para facilitar alguns cálculos e entendimento, pois ela representa posições geográficas em metros.

**5.4 Bandas extraídas:** 

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

**5.5 Montagem do Dataset:** para montar o Dataset, foram selecionadas 4 AOIs (Areas of Interest), de tamanho compatível com a resolução escolhida e em 3 datas diferentes do ano, em níveis L1C (TOA) e L2A(BOA) para ter mais dados em relação a posição do sol. Juntamente com a extração das bandas citadas, também foi extraído (através de scripts) 4 importantes variáveis que vão ser importantes para o pre-processamento dos dados, são esses: 

**5.5.1 Ângulo zenital solar**: Ângulo entre a direção do Sol e a vertical local

<img width="300" height="250" alt="image" src="https://github.com/user-attachments/assets/861bec02-e290-44ab-920a-1e00e20d87d8" />

**5.5.2 Ângulo azimutal solar**: Indica a direção horizontal de onde vem a luz solar

<img width="300" height="250" alt="image" src="https://github.com/user-attachments/assets/2ab15f99-16e2-400b-8dfe-45a72be2684f" />

**5.5.3 Ângulo zenital médio de observação**: Representa o ângulo médio entre a direção de observação do sensor e a vertical local.

<img width="300" height="250" alt="image" src="https://github.com/user-attachments/assets/2636808d-9c38-4a19-8b3d-3510698ad885" />

**5.5.4 Ângulo azimutal médio de observação**: Indica a direção horizontal média para a qual o sensor está apontado

<img width="300" height="250" alt="image" src="https://github.com/user-attachments/assets/f20ec394-a658-4579-9232-d4ab6f066207" />

Esses dados vão servir para a correção de Rayleigh (espalhamento de raios) que vem antes do black-pixel.
   
**6. Pipeline preliminar:** 

6.1 Adquirir dados do sentinel-2 L1C de oceano aberto, via Copernicus, dando entrada de data e região, e recebendo saída imagens TIFF de bandas, juntamente com os dados geométricos citados a cima.

6.2 Pré-processamento: Selecionar uma AOI, mascarar as nuvens se possível, terá como entrada a TOA e saída a imagem mascarada.

6.3 Correção atmosférica: mensurar e remover a influência atmosférica, utilizar do black-pixel assumption e tentar outras alternativas para avaliar, terá como entrada a TOA mascarada e como saída a reflectância da água (BOA).

6.4 Avaliação: comparar resultado obtido com a referência já existente, terá como entrada a BOA e de saída comparações e figuras.

6.5 Visualização/organização de resultados: Apresentar resultados, usar do matplotlib para tal, terá como entrada BOA e comparações e como saída, figuras.

**7. Arquitetura preliminar:** A princípio ainda vai ficar do jeito que está atualmente, até ser necessário mudar ou adicionar coisas.

**8. Estudo inicial e viabilidade:** Ao pesquisarmos sobre o assunto, descobrimos que a literatura é bem consolidade sobre o método a ser explorado (black-pixel assumption), há também ferramentas para testar, como o ACOLITE e POLYMER, que tem suporte para imagens do Sentinel-2, também temos uma boa base de dados para uso (Copernicus), logo conseguimos enxergar viabilidade para começar e concluir o projeto.

**9. Resultados ou experimentos preliminares:** Disponíveis em [Tests_Outputs](https://github.com/ErickLemosB/AC_Open_Ocean/tree/main/Tests_Outputs) e também em [true_color_outputs](https://github.com/ErickLemosB/AC_Open_Ocean/tree/main/images/results/true_color_outputs).

**10. Código e reprodutibilidade:** O código comentado (manualmente para deixar explicativo) está disponível em [Source](https://github.com/ErickLemosB/AC_Open_Ocean/tree/main/src)


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



