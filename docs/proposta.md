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

**2. Contexto de aplicação:** A correção atmosférica (AC) é uma etapa obrigatória de pré processamento em praticamente toda pesquisa e análise de sensoriamento remoto, independentemente da área de aplicação final. A ideia inicial do grupo era tratar corpos ocêanicos de forma geral, mas devido ao tempo disponivel e à complexidade do problema, em especial as áreas costeiras, que se mostram mais desafiadoras por sofrerem forte influência de outros elementos, o escopo foi reduzido para o oceano aberto, onde um único método de correção tende a ser mais consistente

A correção da reflectância da água sobre oceano aberto apoia um conjunto de aplicações:

2.1 Detecção de manchas de óleo e derramamentos
2.2 Rastreamento de resíduos plásticos e outros detritos flutuantes
2.3 Alerta precoce de floroação de algas nocivas
2.4 Suporte à gestão da pesca e ao mapeamento de habitats marinhos
2.5 Monitoramento da "cor do oceano"

**3. Objetivo:** Desenvolver e avaliar um pipeline de correção atmosférica para imagens multiespectrais de satélite sobre águas oceânicas abertas, utilizando esse cenário como estudo de caso do problema geral de correção atmosférica em Processamento Digital de Imagens (PDI). O pipeline deve estimar a reflectância da água (BOA) a partir de dados capturados no topo da atmosfera (TOA, nível L1) e comparar os resultados obtidos com produtos oficiais de referência (nível L2A).

**4. Entrada e saída esperada:** A entrada principal será composta por cenas multiespectrais Sentinel-2 no nível L1C, recortadas para áreas de oceano aberto. Cada cena deverá conter as bandas espectrais necessárias ao método escolhido, metadados de aquisição e informações euxiliares, como resolução espacioal, sistema de referência e condições de cobertura de nuvens. 

A saída esperada será um conjunto de itens, conforme resumido na tabela abaixo:

| Produto | Descrição | Formato inicial previsto |
|---|---|---|
| Reflectância corrigida | Estimativa da reflectância da água na BOA para cada banda processada | GeoTIFF ou matriz compatível |
| Máscara de qualidade | Identificação de nuvens, sombras, pixels inválidos e regiões não utilizadas | GeoTIFF, PNG ou matriz booleana |
| Composição visual | Visualização RGB ou falsa cor para inspeção dos resultados | PNG ou JPG |
| Métricas de avaliação | Valores de erro, correlação e estatísticas por banda ou por região | CSV ou JSON |
| Metadados do processamento | Parâmetros, cena de origem, bandas utilizadas e data de execução | JSON ou Markdown |

O pipeline deverá preservar a georreferência sempre que o formato de entrada permitir. Pixels removidos pela máscara não deverão ser tratados como observações válidas nas métricas, e a ausência de dados deverá ser diferenciada de reflectância efetivamente estimada.

**5. Imagens e dados:** Foram encontradas duas bases públicas de dados para uso no projeto, ambas fornecendo imagens do satélite Sentinel-2 MSI em nível L1C (reflectância no topo da atmosfera):

5.1 Copernicus Browser (ESA/Copernicus) — [https://browser.dataspace.copernicus.eu/](https://browser.dataspace.copernicus.eu/)

5.2 Google Earth Engine (GEE) — [https://code.earthengine.google.com/](https://code.earthengine.google.com/)

As imagens podem ser baixadas em diferentes formatos, incluindo matrizes em formato CSV com as bandas e os índices espectrais escolhidos. Para fins de validação, também serão utilizados produtos de nível L2A (já com correção atmosférica oficial aplicada) das mesmas cenas, servindo como referência de comparação para os resultados obtidos pelo pipeline desenvolvido.

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



