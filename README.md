# Atmospheric Correction Open Ocean 
Repositório referente a proposta da etapa M1 de PDI

**Proposta:** Correção atmosférica (AC) de imagens de sensoriamento remoto para áreas de oceano aberto

**Integrantes: Erick Lemos Barreto, Janine de Paula, Melissa Moreira de Oliveira**

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


**Database:** Encontramos duas databases públicas para uso, que utilizam imagens do satélite Sentinel-2 MS1, no nível L1C (reflectância da TOA).
1. https://browser.dataspace.copernicus.eu/ ESA/Copernicus
2. https://code.earthengine.google.com/ Google Earth Engine (GEE)

As imagens podem ser baixadas em diferentes formatos, incluindo matrizes (em formato de CSV) com as bandas e índicis escolhidos.

Imagem exemplo: <img width="1470" height="917" alt="2026-08-24-00_00_2026-08-24-23_59_Sentinel-2_L1C_True_color" src="https://github.com/user-attachments/assets/63f9507a-7531-42b0-bb30-1c85f31bb142" />

**Estado atual do projeto:** Ainda está em discussão como vai ser desenvolvido e quais soluções, tecnologias e ferramentas que serão usadas.

**Tecnologias previstas:** A princípio o projeto vai ser desenvolvido em Pyhton, aproveitando de bibliotecas já consolidadas de SR e PDI. Para obter os dados é pretendido usar a API da copernicus, numpy para operações sobre as matrizes que contem as bandas, além de outras como matplotlib para fazer comparações. O resto ainda está em discussão.
