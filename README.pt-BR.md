# Dados históricos de saúde pública no Brasil, 1960-1985

English version: [README.md](README.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23680401.svg)](https://doi.org/10.5281/zenodo.23680401)

2.619 registros tirados das tabelas, figuras e do texto de 8 artigos em português impressos entre 1972 e 1989, um por doença ou indicador: um inquérito sorológico nacional de doença de Chagas em 1975-80, a detecção de hanseníase em Recife de 1960 a 1985 (PE), o estado nutricional de crianças menores de 5 anos em 3 municípios de Rondônia em 1985 (RO), a imunidade ao sarampo e a cobertura vacinal de crianças de 5 a 15 meses em Curitiba e São José dos Pinhais em 1983 (PR), um inquérito tuberculínico em escolares do primeiro ano em São Paulo em 1970 (SP), a mortalidade por causa no Distrito Federal em 1977-78 (DF), a malária em dois hospitais de Manaus em 1974-77 (AM) e o programa de controle da esquistossomose na Paraíba em 1978-85 (PB). Cada linha é uma célula impressa ou um número do texto, com a página e a tabela de onde saiu.

Nenhum desses números existe em forma estruturada. As séries oficiais de saúde que estão online começam depois desses estudos: mortalidade (SIM) em 1979, as séries de notificação do SINAN para hanseníase, tuberculose e doença de Chagas aguda em 2001, cobertura vacinal (SI-PNI) em 1994, malária por estado em 1990 e nutrição infantil (SISVAN) em 2008. Nenhuma série tem sorologia, prova tuberculínica ou dado de prontuário hospitalar. Antes de ser transcrito, cada documento foi conferido nas séries que se aplicam a ele, no DataCite e no Harvard Dataverse, e o resultado de cada um está na tabela abaixo.

Os dados são agregados: contagens, taxas, porcentagens e médias por lugar, faixa etária, sexo e ano. Uma tabela do ferraroni1979 lista cada óbito por malária numa linha (TABELA 5, p9); ela foi pulada e nada dela está nos arquivos. Nenhum arquivo tem nome de paciente, endereço ou data de nascimento.

Faz parte do [Paper Rerun](https://paper-rerun.github.io), na linha Open Tables. O trabalho foi feito por agentes de IA num computador doméstico e revisado por uma pessoa antes da publicação.

## O que tem

| | |
|---|---|
| Publicações | 8 artigos de periódico impressos de 1972 a 1989: 5 na Revista de Saúde Pública, 1 na Revista do Instituto de Medicina Tropical de São Paulo, 1 na Acta Amazonica e 1 na Revista da Sociedade Brasileira de Medicina Tropical. Pelo tipo de dado: 4 inquéritos, 1 série de notificação, 1 de estatística vital, 1 de prontuário hospitalar e 1 de programa de controle |
| Estratos | 227: 8 estudos, 96 lugares (municípios, estados, regiões, 2 hospitais e 1 escola), 72 faixas etárias, 15 estratos de sexo, 14 grupos de população, 13 fontes de dado e 9 outros (a idade da vacinação no rodriguez1984) |
| Registros | 2.619: pessoas numa classe 832, prevalência 490, coeficiente de detecção 302, dias de internação 180, casos 157, pessoas examinadas 98, unidades de amostra 80, mortalidade proporcional 64, protegidos 60, internações 59, intervalo de tempo 54, outras medidas 143. 522 deles são totais impressos |
| Estatísticas | contagem 1.256, taxa ou proporção 777, porcentagem de distribuição 431, média 66, mediana 47, dispersão 26, razão 14, média geométrica 2. Taxas: 830 por 100, 320 por 100.000 e 3 por 1.000 |
| De onde vieram | 2.516 registros de tabelas, 84 do texto ou de uma nota e 19 de figuras que imprimem o valor. 38 são estimativas, e 27 são números de outro estudo citado pelo ferreira1988 |

| Documento | O que é | Lugar | Período, como impresso | Estratos | Registros | Conferência de disponibilidade |
|---|---|---|---|---:|---:|---|
| camargo1984 | inquérito sorológico nacional rural da infecção chagásica, SUCAM e CNPq; estimativa de prevalência por estado | Brasil | 1975/1980 | 32 | 99 | nenhuma série oficial tem sorologia de Chagas, e o SINAN (desde 2001) tem só casos agudos; OMS e OPAS dão uma estimativa por país; 0, 2 e 16 resultados no DataCite e no Dataverse, todos recentes. O mesmo inquérito foi impresso de novo por estado e município em 2011, também em tabela de PDF |
| albuquerque1989 | coeficiente de detecção de hanseníase em Recife por sexo, idade e forma clínica, das fichas da Secretaria de Saúde | Recife, PE | entre 1960 e 1985 | 16 | 421 | o SINAN hanseníase começa em 2001, e não há nada por município antes dele; 0, 2 e 11 resultados, todos de 2000 em diante |
| ferreira1988 | estado nutricional de menores de 5 anos em 3 municípios do Polonoroeste, comparado com o ENDEF e Jauru | RO | 1985 | 16 | 168 | o SISVAN começa em 2008 e a antropometria da POF no SIDRA em 2002-03; o microdado da PNSN 1989 (ICPSR 2294) é outra pesquisa e não amostrou esses municípios |
| rodriguez1984 | sorologia de sarampo e cobertura vacinal de crianças de 5 a 15 meses em 7 postos de saúde | Curitiba e São José dos Pinhais, PR | entre os meses de junho e outubro de 1983 | 32 | 315 | o SI-PNI começa em 1994, e sorologia de sarampo não está em série nenhuma; 0 resultado |
| certain1972 | prova tuberculínica em escolares do primeiro ano de 104 escolas estaduais, por idade, sexo e enduração; tabelas impressas giradas | São Paulo, SP | 1970 | 13 | 416 | o SINAN tuberculose começa em 2001 e tem caso notificado, nunca prova tuberculínica; 0 resultado |
| pereira1980 | mortalidade proporcional e coeficientes de mortalidade por causa, sexo e idade, residentes do DF | DF | 1977 e 1978 | 16 | 112 | o SIM começa em 1979 e o Registro Civil no SIDRA em 2003, então 1977-78 fica fora dos dois; o volume impresso de mortalidade nacional de 1977 não foi achado online |
| ferraroni1979 | malária no Hospital de Moléstias Tropicais e no Hospital Geral de Manaus: casos, dias de internação, parasitemia | Manaus, AM | abril de 1974 a dezembro de 1977 | 41 | 653 | dado de hospital nunca entrou em série oficial; malária por estado começa em 1990 (SISMAL 1996, SIVEP-Malária 2003) |
| coura1987 | prevalência da esquistossomose em 47 municípios, das avaliações da SUCAM no programa de controle (PECE) e da amostra própria dos autores em 1984/85 | PB | de 1978 a 1983 e posteriormente em 1984/85 | 61 | 435 | nada por município de 1978-85 no DATASUS, no SIDRA ou no dados.gov.br; 0 resultado. Não deu para ler o ano de início da série online do SISPCE, então essa conferência tem um buraco |

Arquivos:
- `data/records.csv`: um registro por linha (2.619), com `doc_id`, `page` e `table_or_figure`. Cada registro leva os seus próprios valores efetivos (período, unidade, base da taxa, condição, medida), além do cabeçalho da coluna, do rótulo e do tipo da tabela, do período, da unidade, da base da taxa, da definição de caso e da classificação impressos para a tabela, das linhas de "Fonte:" e do significado da nota de rodapé.
- `data/strata.csv`: um estrato por linha (227). Os estratos se encaixam por `parentStratumID`, do estudo para baixo: lugares, faixas etárias, sexo, grupos de população e fontes de dado. Um campo de contexto que o estrato filho não imprime (lugar acima, período, população, fonte de dado, definição de caso, método) vem do estrato acima mais próximo que imprime, e `inherited` diz de qual; rótulo, tamanho da amostra, páginas e notas nunca descem.
- `data/sources.csv`: as 8 publicações, com autores, link do registro e aviso de licença.
- `qa/decisions.csv`: cada divergência entre as duas transcrições independentes e como ela foi resolvida conferindo o PDF (5.925 decisões, com a página).
- `qa/totals_check.csv`: cada total impresso contra a soma das partes transcritas (522 totais). É conferência, não dado; o dataset não muda com ela.
- `qa/rates_check.csv`: cada taxa ou porcentagem impressa ao lado da sua contagem, contra numerador / denominador (352 taxas). Também é conferência, não dado.
- `method/`: o schema, o script de comparação e o script de junção. Eles rodam na pasta de trabalho do piloto, com as transcrições e os PDFs, que não estão incluídos aqui.

### Colunas

Todos os arquivos se ligam a `data/sources.csv` por `doc_id`. Os registros se ligam aos estratos por `doc_id` e `stratum_ids`: `stratum_ids` lista os estratos do registro dentro do documento ("s30; s65; s3"), e `stratumID` é `doc_id#s30`. Um registro pertence a todos os estratos que lista, como um município, uma faixa etária e um sexo; `stratum_labels` e `stratum_dimensions` repetem os rótulos e os tipos deles na mesma ordem. Em `qa/totals_check.csv`, `record_id` é o total em `data/records.csv`, e `part_record_ids` lista os números depois do `#` das partes que foram somadas. Em `qa/rates_check.csv`, `record_id` é a taxa, e `numerator_record_id` e `denominator_record_id` são os registros de onde ela foi recalculada. `decision_ids` num registro lista o `diff_id` das suas linhas em `qa/decisions.csv`, dentro do mesmo `doc_id`.

Rótulos, períodos, condições e unidades ficam exatamente como impressos. Erro de impressão da fonte fica, e quando ele foi confirmado na página o registro diz isso em `source_inconsistency` (33 registros). Os totais impressos ficam como registros com `is_total` = True e nunca são recalculados; `total_kind` diz se o total é de linha, de coluna, geral ou subtotal. 86 dos 522 não são soma: são a taxa, a média ou a porcentagem do grupo inteiro, como a linha "Total" de uma coluna de prevalência. Os números que o ferreira1988 cita do ENDEF 1974-75 ficam com `data_source_kind` = `cited_publication` (27 registros), e um filtro tira todos eles.

### Principais colunas

Os arquivos estão em UTF-8, com vírgula separando as colunas. Em todo registro, `doc_id` liga a linha a `data/sources.csv`, e `page` e `table_or_figure` dizem de onde ela saiu (página do PDF contada a partir de 1, e o rótulo como impresso, "TABELA 6", "Gráfico 3", ou `text` para um número do texto). `record_id` é o registro, no formato `doc_id#0001`.

- `stratum_ids`: os estratos a que o registro pertence.
- `stratumID`, `parentStratumID` e `stratum_dimension`: o estrato, o estrato acima dele e o seu tipo (`study`, `place`, `age_group`, `sex`, `population_group`, `data_source`, `other`).
- `period_as_printed` e `period_context_as_printed`: o período do registro como impresso ("1977", "junho a outubro de 1983") e o período mais largo da legenda ou do método ("entre 1960 e 1985"). 2.584 registros têm período e 1.339 têm também o período de contexto.
- `condition_as_printed`: a doença, a infecção ou a classe de que o número trata, como impressa ("hanseníase", "infecção pelo S. mansoni", "vivax").
- `measure_standardized` e `measure_as_printed`: o que foi contado ou medido, na nossa lista de termos (`prevalence`, `detection_rate`, `persons_examined`, `hospital_days`, `proportional_mortality` e outros em `method/schema.json`) e nas palavras da fonte. `measure_as_printed` ainda não tem regra fixa (ver os limites); use `measure_standardized` para agrupar registros.
- `value`, `value_as_printed` e `value_kind`: o número pronto para cálculo, com ponto decimal, e a célula como impressa ("2.631", "5,5"). 2.609 valores são numéricos; 5 são ilegíveis e guardam a melhor leitura, 2 vêm malformados na impressão ("100 0", "0 9"), 2 são palavras ("nenhum", "um") e 1 é uma faixa, com `value_min` e `value_max`.
- `unit_as_printed`, `rate_multiplier` e `rate_denominator_as_printed`: a unidade como impressa ("%", "por cem mil habitantes", "dias"), a base da taxa como número (100, 1000, 100000) e a população sobre a qual a taxa é calculada, como impressa.
- `statistic`: `count`, `rate_or_proportion`, `percentage_share`, `mean`, `median`, `dispersion_measure`, `ratio` ou `geometric_mean`.
- `is_total` e `total_kind`: se o registro é um total impresso, e de que tipo.
- `data_source_kind`: de onde vem o número: inquérito do próprio estudo (1.085 registros), prontuário hospitalar (647), notificação (413), programa de controle (321), registro vital (102), publicação citada (27), estimativa de população (13) ou não declarado (11). `is_estimate` marca os 38 números que a fonte imprime como estimativa.
- `origin` e `decision_ids`: se o registro final é aquele em que as duas transcrições concordaram (1.233), o da transcrição A (265) ou da B (636), ou um corrigido (485), e as decisões por trás dele.
- `inherited` (estratos): os campos que o estrato recebeu de um estrato acima, e de qual ("period_as_printed:s1").

## Como foi feito

1. **Coleta.** Um agente percorreu a Revista de Saúde Pública pelo OAI-PMH (5.271 registros) e, em parte, os periódicos da Secretaria de Estado da Saúde de São Paulo (6.495 registros, parado antes do fim), leu os sumários da Revista da Sociedade Brasileira de Medicina Tropical de 1967 a 1999 no SciELO e buscou na web boletins estaduais, SUCAM/FUNASA, Fiocruz e Acta Amazonica. 26 candidatos foram lidos e ficaram de fora, cada um com o motivo: 13 bons documentos guardados para a rodada cheia, para equilibrar doença, região e fonte, 7 com conteúdo que não serve (teste estatístico, relato de caso, revisão, nota curta), 3 fora do ar quando tentamos, 2 já estruturados (SB Brasil 1986 em xlsx no site do Ministério, PNSN 1989 no ICPSR) e 1 que imprime de novo um inquérito escolhido.
2. **Conferência de disponibilidade.** Só entrou documento cujos dados não existem em forma estruturada. O ano de início de cada série oficial foi lido na própria série (as listas de período dos formulários do TabNet, a API do SIDRA), e cada documento passou por três buscas no DataCite (que registra os DOIs do Zenodo, do figshare, do Dryad, do SciELO Data e do Mendeley Data) e no Harvard Dataverse.

   | Série oficial | Online desde |
   |---|---|
   | SIM, mortalidade (TabNet, CID-9) | 1979 (CID-10 a partir de 1996) |
   | SINAN tuberculose | 2001 |
   | SINAN hanseníase | 2001 |
   | SINAN doença de Chagas aguda | 2001; nunca sorologia |
   | SI-PNI, cobertura vacinal | 1994 |
   | IBGE SIDRA, Registro Civil (óbitos e nascidos vivos) | 2003 |
   | Malária por estado (IDB/RIPSA) | 1990; SISMAL 1996, SIVEP-Malária 2003 |
   | SISVAN, nutrição | 2008 |
   | Antropometria da POF no SIDRA | 2002-03 |
   | SISPCE, esquistossomose | não verificado: nenhum dos três caminhos DEF devolveu formulário |

3. **Duas transcrições independentes.** Dois agentes por artigo transcreveram os estratos, um inventário das tabelas, figuras e blocos de texto com número, e cada célula de dado num schema fixo, sem ver o trabalho um do outro, copiando rótulos, períodos, unidades e números exatamente como impressos. Lista de casos individuais entrou no inventário com 0 célula e não foi transcrita; os dois agentes fizeram isso com a TABELA 5 do ferraroni1979.
4. **Comparação e arbitragem.** Um script pareou as duas transcrições estrato por estrato e registro por registro e listou cada divergência e cada item presente em só uma delas. Cada caso foi resolvido conferindo a página renderizada, com a página como evidência. Os árbitros parearam de novo, à mão, 78 linhas de um lado só que eram o mesmo registro dividido de forma diferente por A e B.
5. **Junção e conferências.** Um script juntou os documentos arbitrados, completou cada estrato com o estrato acima, somou as partes de cada total impresso e recalculou cada taxa impressa ao lado da sua contagem. Os registros saem como arbitrados, sem herança. O mesmo script procura célula que copie mais de 15 palavras da fonte e data, endereço e data de nascimento em toda célula. Ele achou um rótulo copiado de 17 palavras no rodriguez1984 p7, trocado pelo rótulo da outra transcrição, de 12 palavras; depois disso, 0. Nada no dataset mudou com as conferências de totais e de taxas.

## Qual a precisão

- **Números:** nenhum algarismo foi lido errado em nenhuma das duas transcrições. Nos 2.619 registros pareados, 10 campos de valor foram decididos contra um lado, e nenhum é leitura errada: são regras de cópia, como "0.34" impresso com ponto no meio de vírgulas e escrito "0,34", ou as palavras "nenhum" e "um" escritas como 0 e 1. Os casos difíceis passaram: a camada de OCR do camargo1984, que lê "2.t9" onde a página imprime um número, as tabelas giradas do certain1972, uma contagem e uma porcentagem na mesma célula, "20 (11,5)", e os números do ferraroni1979 impressos fracos demais para ler com certeza (7 decisões), guardados como ilegíveis com a melhor leitura. Uma palavra foi lida errado num rótulo, numa nota da TABELA 4 do ferraroni1979.
- **Campos:** 35 campos foram comparados em cada registro. A transcrição A errou 1.432 de 91.665, 98,44% certos; a transcrição B errou 765, 99,17% certos.
- **Registros inteiros:** sozinha, a A estava totalmente correta em 57,1% dos registros e a B em 71,4%, contando os registros que cada uma deixou de fora (3 e 1). A diferença para os números por campo vem das cascatas de contexto. Um registro conta como errado se qualquer um dos seus 35 campos estiver errado, e a maior parte dos erros foi uma regra mal lida no documento inteiro, o que põe o mesmo campo errado em toda linha de uma tabela. A B pôs o estrato do estudo inteiro nas 99 células do camargo1984, cujas linhas imprimem cada uma um estado; a A deixou o denominador da taxa vazio em 330 registros do coura1987; a B deixou a unidade "crianças" vazia em 324 registros do rodriguez1984. Por isso o mesmo lado tira 96,0% num documento e 0,0% em outro, e um lado que lê a regra certo passa de 92% em quase todo documento. Contando só os campos de conteúdo (valor, rótulo, condição, medida, estatística, período, unidade, total), 88,2% dos registros da A e 88,6% dos da B estavam certos. Estratos: 78,4% e 86,8%. Tabelas: 54,7% e 60,0%. As 5.925 divergências foram resolvidas conferindo o PDF, então os dados finais não dependem de nenhuma das duas transcrições sozinha.
- **Totais impressos:** dos 522 totais, 420 podem ser conferidos com as suas partes: 407 fecham exatamente, 6 fecham no arredondamento e 7 não fecham. Os outros 102 são 86 que não são soma (a taxa ou a média do todo), 8 em figuras que imprimem só algumas barras e 8 com uma parte ilegível ou malformada. Os 6 no arredondamento são 4 colunas de porcentagem do ferreira1988 que somam 99,9 e 2 contagens do ferraroni1979 que diferem em 1. As duas transcrições concordam em toda célula envolvida nos 7, e cada caso foi aberto na página: são 3 erros da fonte. Cada caso está em `qa/totals_check.csv`, em `status` e `note`.
  - ferraroni1979 TABELA 4, doenças venéreas: Militar 99 + Civil 3 dão 102; a coluna Total imprime 112. Com 112 a coluna Total soma 354, e o TOTAL impresso é 344, que é Militar (285) + Civil (59). O erro está no 112. 2 linhas.
  - ferraroni1979 TABELA 6, totais de 1976: a linha "02** — 04" imprime 17 no total ±±, e vivax 18 + falciparum 9 dão 27; a linha "30 — 39" imprime 15 no total ±, e 31 + 34 dão 65. Os totais de coluna (391 e 377) fecham com 65 e 27, então os autores somaram certo e as duas células saíram erradas na impressão. 4 linhas.
  - ferreira1988 TABELA 2, Ouro Preto D'Oeste: a coluna de porcentagem soma 100,8. A Eutrofia imprime 87,8, e 335 / 385 dá 87,0. 1 linha.
- **Taxas contra as suas contagens:** 352 taxas ou porcentagens imprimem a sua contagem ao lado. 322 batem com ela (298 no arredondamento e 24 em que o autor cortou o último dígito em vez de arredondar, como 82,0 impresso para 32 / 39 = 82,05 no rodriguez1984), 13 diferem no último dígito e 17 não batem. Outras 816 taxas não imprimem numerador na tabela (estimativas de prevalência, coeficientes por 100.000 sem a população) e não foram conferidas. Não use como estão as porcentagens do bloco 1970-77 da TABELA 6 do albuquerque1989 nem as porcentagens de vivax feminino de 1976 da TABELA 1 do ferraroni1979; as contagens dessas tabelas estão certas. Cada caso está em `qa/rates_check.csv`, em `status`.
  - albuquerque1989 TABELA 6, bloco 1970-77 (5): as porcentagens somam 100,0 e as contagens 738, mas uma não é a outra: 32 / 738 dá 4,3 e a página imprime 4,7; 268 dá 36,3 contra 39,0; 322 dá 43,6 contra 39,4. Os blocos 1978-85 e 1970-85 batem.
  - ferraroni1979 TABELA 4 (3): as porcentagens parecem calculadas sobre uns 347 internados, não sobre os 344 impressos (60 / 344 dá 17,4, impresso 17,3), e a de doenças venéreas usa o 112 de cima.
  - ferraroni1979 TABELA 1, vivax feminino em 1976 (2): 78 e 27 sobre 105 dão 74 e 26; a página imprime 71 e 29. As contagens fecham com os totais de linha (245 e 122), então o erro está nas porcentagens.
  - certain1972 TABELA 3 (4): diferenças de 0,01 a 0,03, como se os autores tivessem dividido por 941 em vez dos 943 impressos.
  - rodriguez1984 Tabela 6 (2): a linha "7º a 8º" imprime 12 crianças examinadas, com 59 não protegidas e 61 protegidas. O texto da p5 diz 120 crianças vacinadas: a tabela perdeu um zero.
  - ferreira1988 TABELA 2 (1): o 87,8 de cima.
- **Limites conhecidos:**
  - ferraroni1979 tem 653 registros, 25% do dataset. Sem ele, o acerto por registro inteiro fica em 48,1% para a A e 67,1% para a B.
  - O schema ainda deixa margem demais nos campos de contexto, e é por isso que o acerto por registro inteiro é baixo. `measure_as_printed` não tem regra fixa: um lado tirou do cabeçalho da coluna, o outro da condição. `total_kind` não separa uma soma da taxa do todo (os 86 de cima).
  - Unidades e períodos estão como impressos, sem data ISO e sem valor convertido: "%", "por 100" e "por cem mil habitantes" ficam lado a lado, e 927 registros não imprimem unidade, quase todos contagens cujo `measure_standardized` diz o que foi contado.
  - Algumas células são contagens de 1 ou 2 em tabelas por idade, sexo e mês (ferraroni1979, rodriguez1984). São dado agregado e ficaram; nenhuma se combina com outra coisa dos arquivos que aponte para uma pessoa.
  - O tamanho da amostra de um inquérito fica no estrato do estudo e não desce: "1.626.745 amostras" no camargo1984 é o inquérito inteiro, não cada estado.
  - A conferência de disponibilidade tem buracos: não deu para ler o início online do SISPCE (coura1987), o bvsms.saude.gov.br respondeu 503, o scielo.iec.gov.br não respondeu, o scielosp.org respondeu 403 ao download por script, o search.scielo.org pediu desafio de robô (não tentamos passar) e o ARCA da Fiocruz respondeu 404. As "Estatísticas do Século XX" do IBGE não foram abertas tabela por tabela.
  - Os 8 são artigos de periódico, nenhum dos anos 1990, e 5 vêm da Revista de Saúde Pública. Ainda não há boletim oficial; o melhor candidato, o Informe Epidemiológico do SUS de 1992-94, estava fora do ar.

Este é um piloto de 8 documentos, feito para acertar o schema. Uma rodada maior, de 20 documentos, está planejada.

## Licença e citação

- O dataset (os arquivos CSV, o schema e os scripts) é publicado sob a licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Por favor, cite as publicações originais listadas em `data/sources.csv` e também este dataset. Cada linha também traz a sua fonte em `citation` e a situação de licença da fonte em `license`.
- As publicações não são redistribuídas. ferraroni1979 (Acta Amazonica) tem CC BY 4.0 na página do artigo no SciELO. A Revista do Instituto de Medicina Tropical de São Paulo declara CC BY 4.0 para todo o seu conteúdo na página "about", sem licença no item, o que cobre o camargo1984. albuquerque1989, ferreira1988, rodriguez1984 e pereira1980 (Revista de Saúde Pública) e coura1987 (Revista da Sociedade Brasileira de Medicina Tropical) têm CC BY-NC 4.0 nas páginas dos artigos no SciELO; o site de periódicos da USP mostra só uma linha de direitos autorais para os mesmos artigos. A licença do certain1972 não está confirmada: a página dele no SciELO respondeu 502 duas vezes. Nenhum PDF imprime licença, já que todos são escaneamentos das edições impressas. Aqui são usados só contagens, taxas e médias, que são fatos, e citações curtas de no máximo 15 palavras.

Erros ou registros que faltam: por favor, [abra uma issue](https://github.com/paper-rerun/public-health-historical-br/issues).

## Como este dataset foi feito

Este dataset foi montado por agentes de IA (Claude, da Anthropic) num computador doméstico e revisado por uma pessoa antes da publicação. Nenhum valor foi estimado ou digitado à mão: cada um foi transcrito do PDF original duas vezes, de forma independente, e cada divergência foi conferida na página. O método e os scripts estão em `method/`. Como funciona o projeto como um todo (em inglês): https://github.com/paper-rerun/paper-rerun/blob/main/METHOD.md

Contato: Filipe Tessaro, pelas issues deste repositório.
