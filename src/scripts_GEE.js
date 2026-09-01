// ============================================================================
// Script GEE (Google Earth Engine Code Editor) — Sentinel-2, multi-oceano
// Projeto: Atmospheric Correction Open Ocean (M1 - PDI)
//
// O QUE ESTE SCRIPT FAZ:
//   Pega 5 cenas Sentinel-2 (nível L1C, TOA — sem correção atmosférica) de
//   cada uma das 4 regiões oceânicas abaixo, e para cada cena exporta:
//     a) uma imagem "visível" (RGB, cor verdadeira) para o Google Drive;
//     b) um CSV com B2, B3, B4, B8, NDWI, SWIR1, SWIR2, latitude,
//        longitude e .geo, amostrados na grade de pixels da imagem.
//
// AVISO IMPORTANTE — LEIA ANTES DE RODAR:
//   O Sentinel-2 NÃO fotografa sistematicamente o oceano aberto longe de
//   qualquer costa. A estratégia de aquisição da ESA prioriza terra e uma
//   faixa costeira/ilhas — um ponto escolhido no meio do oceano, sem
//   nenhuma ilha por perto, muito provavelmente retorna ZERO cenas.

//   Depois de calcular o NDWI, o script mascara automaticamente os pixels
//   de terra (NDWI <= 0), então o CSV final só contém pixels de água, mesmo
//   que a ilha apareça dentro do recorte da imagem.
//
//   Se quiser trocar os locais, prefira outras ilhas isoladas — evite um
//   ponto "vazio" no meio do oceano sem nenhuma terra por perto.
// ============================================================================


// ----------------------------------------------------------------------------
// 1. REGIÕES (AJUSTAR SE QUISER OUTRAS ILHAS/LOCAIS)
// ----------------------------------------------------------------------------
var regioes = [
  {
    nome: 'South_Atlantic',
    ponto: ee.Geometry.Point([-5.7089, -15.9650]) // Santa Helena
  },
  {
    nome: 'Indian_Ocean',
    ponto: ee.Geometry.Point([72.4055, -7.3133]) // Diego Garcia
  },
  {
    nome: 'North_Atlantic',
    ponto: ee.Geometry.Point([-28.7000, 38.5800]) // Faial, Açores
  },
  {
    nome: 'South_Pacific',
    ponto: ee.Geometry.Point([-109.3497, -27.1127]) // Ilha de Páscoa
  }
];


// ----------------------------------------------------------------------------
// 2. PARÂMETROS GERAIS (AJUSTAR CONFORME NECESSIDADE)
// ----------------------------------------------------------------------------
var raioAoiMetros = 4000;      // raio do recorte ao redor de cada ponto, em metros
var dataInicio = '2025-01-01'; // início do período de busca
var dataFim = '2026-08-28';    // fim do período de busca
var nuvemMaximaPct = 15;       // % máxima de cobertura de nuvem na cena
var cenasPorRegiao = 5;        // quantidade de cenas por oceano
var numPixelsPorCena = 2000;   // quantidade de pontos amostrados por cena no CSV


// ----------------------------------------------------------------------------
// 3. FUNÇÃO: NDWI, aliases SWIR1/SWIR2, bandas de lat/lon e máscara de água
// ----------------------------------------------------------------------------
var prepararImagem = function (imagem) {
  var ndwi = imagem.normalizedDifference(['B3', 'B8']).rename('NDWI');
  var swir1 = imagem.select('B11').rename('SWIR1');
  var swir2 = imagem.select('B12').rename('SWIR2');
  var lonLat = ee.Image.pixelLonLat().rename(['longitude', 'latitude']);
  var mascaraAgua = ndwi.gt(0); // heurística simples: NDWI > 0 costuma indicar água

  return imagem
    .addBands([ndwi, swir1, swir2, lonLat])
    .updateMask(mascaraAgua)
    .copyProperties(imagem, ['system:time_start']);
};

var bandasParaAmostrar = [
  'B2', 'B3', 'B4', 'B8', 'NDWI', 'SWIR1', 'SWIR2', 'longitude', 'latitude'
];
var visParams = { bands: ['B4', 'B3', 'B2'], min: 0, max: 3000 };


// ----------------------------------------------------------------------------
// 4. LOOP PRINCIPAL: para cada região, busca as cenas e cria as exportações
// ----------------------------------------------------------------------------
Map.setCenter(0, 0, 2);

for (var r = 0; r < regioes.length; r++) {
  var regiao = regioes[r];
  var aoi = regiao.ponto.buffer(raioAoiMetros).bounds();

  var colecao = ee.ImageCollection('COPERNICUS/S2_HARMONIZED')
    .filterBounds(aoi)
    .filterDate(dataInicio, dataFim)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', nuvemMaximaPct))
    .sort('system:time_start')
    .limit(cenasPorRegiao);

  var totalEncontrado = colecao.size().getInfo();
  print(regiao.nome + ' — cenas encontradas:', totalEncontrado);

  if (totalEncontrado === 0) {
    print('ATENÇÃO: nenhuma cena encontrada para ' + regiao.nome +
      '. Tente aumentar "nuvemMaximaPct", ampliar o período, ou trocar o ponto.');
    continue;
  }

  var colecaoProcessada = colecao.map(prepararImagem);
  var lista = colecaoProcessada.toList(totalEncontrado);

  for (var i = 0; i < totalEncontrado; i++) {
    var img = ee.Image(lista.get(i));
    var data = ee.Date(img.get('system:time_start')).format('YYYYMMdd').getInfo();
    var idBase = regiao.nome + '_' + data;

    Map.addLayer(img.clip(aoi), visParams, idBase);

    // 4a. Exporta imagem RGB (cor verdadeira) para o Google Drive
    Export.image.toDrive({
      image: img.select(['B4', 'B3', 'B2']).clip(aoi),
      description: 'S2_RGB_' + idBase,
      folder: 'AC_Open_Ocean',
      fileNamePrefix: 'S2_RGB_' + idBase,
      region: aoi,
      scale: 10,
      crs: 'EPSG:4326',
      maxPixels: 1e13
    });

    // 4b. Exporta CSV com as bandas + lat/lon + .geo
    var amostras = img.select(bandasParaAmostrar).sample({
      region: aoi,
      scale: 10,
      numPixels: numPixelsPorCena,
      geometries: true
    });

    Export.table.toDrive({
      collection: amostras,
      description: 'S2_CSV_' + idBase,
      folder: 'AC_Open_Ocean',
      fileNamePrefix: 'S2_bandas_' + idBase,
      fileFormat: 'CSV'
    });
  }
}
