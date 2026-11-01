# Dados históricos de saúde pública no Brasil, 1960-1989

English version: [README.md](README.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23680401.svg)](https://doi.org/10.5281/zenodo.23680401)

7.467 registros tirados das tabelas, figuras e texto de 28 artigos impressos em português entre 1968 e 1995, com dados coletados de 1960 a 1989. Cobrem doença de Chagas, esquistossomose, filariose, cisticercose, hepatite B, malária, hanseníase, teste tuberculínico, meningite, tétano, sarampo, mortalidade infantil e materna, mortalidade por causa, diarreia infantil, nutrição, cárie dentária, hipertensão e cobertura vacinal, do Amazonas ao Rio Grande do Sul. Cada linha é uma célula impressa ou um número do texto, com a página e a tabela de onde saiu.

Nenhum desses números existe em forma estruturada naquele período ou nível de detalhe. As séries oficiais de saúde que estão online começam depois da maioria desses estudos: mortalidade (SIM) em 1979, as séries do SINAN para hanseníase, tuberculose e Chagas agudo em 2001, cobertura vacinal (SI-PNI) em 1994, malária por estado em 1990 e nutrição infantil (SISVAN) em 2008, e nenhuma série traz sorologia, teste cutâneo ou registro hospitalar. Antes da transcrição, cada documento foi conferido na série correspondente, no DataCite e no Harvard Dataverse; o resultado de cada um está em `availability_check` de `data/sources.csv`.

Os dados são agregados: contagens, taxas, porcentagens e médias por lugar, faixa etária, sexo e ano. Tabela que lista indivíduos fica de fora, e nada dela está nos arquivos (uma tabela no piloto, nenhuma na rodada). Nenhum arquivo tem nome de paciente, endereço ou data de nascimento.

Faz parte do [Paper Rerun](https://paper-rerun.github.io), na linha Open Tables. O trabalho foi feito por agentes de IA num computador doméstico e revisado por uma pessoa antes da publicação.

## Versões

- **v2.0.0** (novembro de 2026): 28 artigos. Junta uma rodada de 20 artigos aos 8 do piloto, com o schema 2.0: regra fixa para `measure_as_printed`, denominador e unidade tirados da legenda e do método, `total_kind` = `overall` para a taxa ou média do grupo inteiro e uma busca de cópia longa rodada por cada adjudicador. Os arquivos do piloto não mudaram.
- **v1.0.0** (outubro de 2026): piloto de 8 artigos, 2.619 registros.

## O que tem

| | |
|---|---|
| Publicações | 28 artigos de periódico impressos de 1968 a 1995: Revista de Saúde Pública, Revista da Sociedade Brasileira de Medicina Tropical, Cadernos de Saúde Pública, as revistas da Secretaria de Estado da Saúde de São Paulo, Revista do Instituto de Medicina Tropical de São Paulo e Acta Amazonica |
| Estratos | 901: 28 estudos, 312 lugares, 267 faixas etárias, 179 grupos populacionais, 57 estratos de sexo, 45 fontes de dado e 13 outros |
| Registros | 7.467: pessoas numa classe 1.380, casos 1.166, prevalência 865, pessoas examinadas 639, taxa de mortalidade 377, resultados positivos 374, taxa de incidência 359, óbitos 339, taxa de detecção 302, população 278 e outros. 1.331 deles são totais impressos |
| Estatísticas | contagem 3.693, taxa ou proporção 2.015, participação percentual 1.309, média 212, dispersão 95, mediana 52, razão 43, outras 48. Taxas: 2.248 por 100, 764 por 100.000, 173 por 10.000 e 114 por 1.000 |
| De onde vieram | inquérito do próprio estudo 3.535, registro hospitalar ou de serviço 1.249, notificação 950, programa de controle 619, registro civil 396, publicação citada 282, misto 257, estimativa populacional 107, não informado 72 |

| Documento | O que é | Lugar | Estratos | Registros |
|---|---|---|---:|---:|
| camargo1984 | inquérito sorológico nacional de Chagas na zona rural, 1975-80 | Brasil | 32 | 99 |
| albuquerque1989 | taxa de detecção de hanseníase por sexo, idade e forma clínica, 1960-85 | Recife, PE | 16 | 421 |
| ferreira1988 | estado nutricional de menores de 5 anos, 1985 | RO | 16 | 168 |
| rodriguez1984 | sorologia de sarampo e cobertura vacinal em 7 postos de saúde, 1983 | Curitiba e São José dos Pinhais, PR | 32 | 315 |
| certain1972 | teste tuberculínico em alunos do primeiro ano de 104 escolas estaduais, 1970 | São Paulo, SP | 13 | 416 |
| pereira1980 | mortalidade por causa, sexo e idade, 1977-78 | DF | 16 | 112 |
| ferraroni1979 | malária em dois hospitais, 1974-77 | Manaus, AM | 41 | 653 |
| coura1987 | prevalência de esquistossomose em 47 municípios, 1978-85 | PB | 61 | 435 |
| costa1980 | esquistossomose em trabalhadores de nove engenhos, 1977 | Catende, PE | 21 | 169 |
| araujo1973 | mortalidade infantil e causas, com ligações de água, 1960-69 | Salvador e interior da Bahia, BA | 8 | 82 |
| souza1983 | mortalidade materna nas maternidades, 1975-79 | Florianópolis, SC | 15 | 185 |
| souza1969 | cárie dentária (CPO-D) de escolares de 7 a 12 anos, 1968 | Brasília, DF | 14 | 200 |
| iversson1976 | doença meningocócica por mês, distrito, idade e sexo, 1968-74 | São Paulo, SP | 41 | 684 |
| campos1995 | diarreia e óbitos em menores de 5 anos, inquéritos domiciliares de 1986 e 1989 | São Luís, MA | 42 | 269 |
| santos1995 | déficit de peso e altura em pré-escolares de 7 municípios, 1989 | semiárido baiano, BA | 19 | 114 |
| koifman1974 | tétano: casos, óbitos, coeficientes e letalidade, 1960-69 | Guanabara, RJ | 74 | 398 |
| correialima1976 | sorologia de Chagas em 24 municípios, 1975 | PI | 48 | 271 |
| menezes1980 | esquistossomose por exame de fezes e intradermorreação, com caramujos, 1974 | Riachuelo, SE | 27 | 371 |
| araujofilho1980 | surto de sarampo, taxas de ataque por localidade e idade, 1976 | Ilha Grande, RJ | 43 | 241 |
| dobbin1968 | filariose bancroftiana por idade e sexo e infecção do Culex, 1963 | São Lourenço da Mata, PE | 10 | 46 |
| alecrim1986 | HBsAg por idade em pessoas com e sem hepatite clínica | Lábrea, AM | 13 | 52 |
| vianna1986 | sorologia de cisticercose em soro e líquor | Brasília, DF | 108 | 299 |
| galvao1985 | hanseníase: prevalência, incidência e casos novos por forma e município, 1972-84 | região de Presidente Prudente, SP | 54 | 502 |
| moraes1989 | meningite por Haemophilus confirmada por cultura, 1960-77 | São Paulo, SP | 75 | 372 |
| szwarcwald1985 | cobertura vacinal de crianças de 12 a 23 meses, 1983 | Teresina, PI | 14 | 102 |
| klein1985 | prevalência de hipertensão em adultos e mortalidade cardiovascular, 1979 | Volta Redonda, RJ | 22 | 258 |
| baruffa1974 | sorologia de Chagas em 1.383 pessoas de cinco municípios, 1970-71 | Zona Sul do Rio Grande do Sul, RS | 19 | 93 |
| giugliano1977 | estado nutricional e sinais clínicos de pré-escolares de uma creche, 1976 | Manaus, AM | 7 | 140 |

Arquivos:
- `data/records.csv`: um registro por linha (7.467), com `doc_id`, `page` e `table_or_figure`. Cada registro traz os próprios valores efetivos (período, unidade, base da taxa, condição, medida), mais o cabeçalho da coluna, o rótulo e o tipo da tabela, o período, a unidade, a base da taxa, a definição de caso e a classificação impressos para a tabela, as linhas de "Fonte:" e o significado da nota de rodapé.
- `data/strata.csv`: um estrato por linha (901). Os estratos se encaixam por `parentStratumID`, do estudo para baixo: lugares, faixas etárias, sexo, grupos populacionais e fontes de dado. Um campo de contexto que o estrato filho não imprime vem do estrato acima mais próximo que imprime, e `inherited` diz de qual; rótulo, tamanho de amostra, páginas e notas nunca descem.
- `data/sources.csv`: as 28 publicações, com autores, link do registro, aviso de licença e a conferência de disponibilidade.
- `qa/decisions.csv`: cada divergência entre as duas transcrições independentes e como ela foi resolvida conferindo o PDF (11.554 decisões, com a página).
- `qa/totals_check.csv`: cada total impresso contra a soma das partes transcritas (1.105 conferências). É conferência, não dado; o dataset não muda com ela.
- `qa/rates_check.csv`: cada taxa ou porcentagem impressa ao lado da sua contagem, contra numerador / denominador (1.400 conferências). Também é conferência, não dado.
- `method/`: o schema (`schema.json`, gerado por `build_schema.py`), o autoteste dele, os scripts de comparação e de junção e a busca de cópia longa. Eles rodam na pasta de trabalho, com as transcrições e os PDFs, que não vêm aqui.

### Colunas

Todos os arquivos se ligam a `data/sources.csv` por `doc_id`. Registros se ligam aos estratos por `doc_id` e `stratum_ids`: `stratum_ids` lista os estratos do registro dentro do documento ("s30; s65; s3"), e `stratumID` é `doc_id#s30`. Um registro pertence a todos os estratos que lista, como um município, uma faixa etária e um sexo; `stratum_labels` e `stratum_dimensions` repetem os rótulos e tipos na mesma ordem. Em `qa/totals_check.csv`, `record_id` é o total e `part_record_ids` lista as partes somadas. Em `qa/rates_check.csv`, `record_id` é a taxa, e `numerator_record_id` e `denominator_record_id` são os registros de onde ela foi recalculada. `decision_ids` num registro lista os `diff_id` das linhas dele em `qa/decisions.csv`, dentro do mesmo `doc_id`.

Rótulos, períodos, condições e unidades ficam exatamente como impressos. Erro de impressão da fonte fica, e quando foi confirmado na página o registro diz isso em `source_inconsistency` (117 registros). Total impresso é guardado como registro com `is_total` = True e nunca é recalculado; `total_kind` diz se é total de linha, de coluna, total geral, subtotal ou `overall`, a taxa ou média do grupo inteiro (226), que não é soma. Número que um artigo cita de outro estudo fica com `data_source_kind` = `cited_publication` (282 registros), então um filtro tira todos.

As principais colunas:
- `record_id`: o registro, no formato `doc_id#0001`. `page` é a página do PDF contada a partir de 1; `table_or_figure` é o rótulo como impresso ("TABELA 6", "Gráfico 3"), ou `text` para número no texto.
- `period_as_printed` e `period_context_as_printed`: o período do registro como impresso e o período mais largo da legenda ou do método.
- `condition_as_printed`: a doença, infecção ou classe de que o número trata, como impressa.
- `measure_standardized` e `measure_as_printed`: o que foi contado ou medido, na nossa lista de termos (`prevalence`, `cases`, `incidence_rate`, `persons_examined` e outros em `method/schema.json`) e nas palavras da fonte.
- `value`, `value_as_printed` e `value_kind`: o número pronto para cálculo, com ponto decimal, e a célula como impressa. 7.382 valores são numéricos; 40 estão ilegíveis e guardam a melhor leitura, 12 estão malformados na impressão, 18 são classes, 7 são símbolos e 8 são faixas, com `value_min` e `value_max`.
- `unit_as_printed`, `rate_multiplier` e `rate_denominator_as_printed`: a unidade como impressa, a base da taxa como número (100, 1000, 10000, 100000) e a população sobre a qual a taxa é tomada, como impressa.
- `statistic`: `count`, `rate_or_proportion`, `percentage_share`, `cumulative_percentage`, `mean`, `median`, `dispersion_measure`, `ratio`, `geometric_mean` ou `other`.
- `data_source_kind`: de onde vem o número. `is_estimate` marca os 120 números que a fonte imprime como estimativa.
- `origin` e `decision_ids`: se o registro final é o que as duas transcrições concordaram (2.946), o da transcrição A (1.330) ou da B (1.840), ou um corrigido (1.351), e as decisões por trás dele.

## Como foi feito

1. **Coleta.** Os agentes colheram a Revista de Saúde Pública e as revistas da Secretaria de Estado da Saúde de São Paulo pelo OAI-PMH, leram os sumários no SciELO da Revista da Sociedade Brasileira de Medicina Tropical, dos Cadernos de Saúde Pública e de outras revistas e procuraram boletins estaduais e material da SUCAM/FUNASA e do Ministério da Saúde. Todo candidato que ficou de fora está registrado com o motivo.
2. **Conferência de disponibilidade.** Só entrou documento cujos números não existem em forma estruturada naquele período ou nível de detalhe. O ano de início de cada série oficial foi lido na própria série (as listas de período dos formulários do TabNet, a API do SIDRA), e cada documento passou por buscas no DataCite (que registra os DOIs do Zenodo, do figshare, do Dryad, do SciELO Data e do Mendeley Data) e no Harvard Dataverse.
3. **Duas transcrições independentes.** Dois agentes por artigo transcreveram os estratos, um inventário das tabelas, figuras e blocos de texto com número e cada célula de dado num schema fixo, sem ver o trabalho um do outro, copiando rótulos, períodos, unidades e números exatamente como impressos. Lista de casos individuais entrou no inventário com 0 célula e não foi transcrita.
4. **Comparação e arbitragem.** Um script pareou as duas transcrições estrato por estrato e registro por registro e listou cada divergência e cada item presente em só uma delas. Cada caso foi resolvido conferindo a página renderizada, com a página como evidência. Na rodada, cada documento ainda passou por uma conferência à parte do lugar, do período, da população, da definição de caso, do denominador, da unidade e da base da taxa de cada tabela, para pegar o erro de contexto que as duas transcrições cometem juntas.
5. **Junção e conferências.** Um script juntou os documentos arbitrados, completou cada estrato com o estrato acima, somou as partes de cada total impresso e recalculou cada taxa impressa ao lado da sua contagem. Os registros saem como arbitrados, sem herança. Em toda célula se procura cópia longa da fonte e data, endereço e data de nascimento: 0 cópia longa; os únicos achados de "rua" são uma classe de destino do lixo em campos1995. Nada no dataset mudou com as conferências de totais e taxas.

## Qual a precisão

- **Números:** nos 7.422 registros pareados das duas rodadas, um algarismo foi lido errado uma vez, na rodada (costa1980 TABELA 2, 24 lido como 21), e corrigido. Os outros campos de valor decididos contra um lado são regra de cópia, como um separador normalizado ou "nenhum" escrito como 0.
- **Campos:** na rodada, a transcrição A acertou 98,69% dos campos e a B 98,46% (98,44% e 99,17% no piloto).
- **Registros inteiros:** contando os registros que cada uma deixou de fora, A sozinha acertou por inteiro 61,4% dos registros da rodada e B 66,1% (57,1% e 71,4% no piloto). A distância para os números por campo vem das cascatas de contexto: um registro conta como errado se qualquer campo dele está errado, e quase todo erro foi uma regra mal lida num documento inteiro, como a condição ou o rótulo de linha, o que põe o mesmo campo errado em toda linha de uma tabela. As 11.554 divergências foram resolvidas conferindo o PDF, então o dado final não depende de nenhuma das duas transcrições sozinha.
- **Erros de contexto:** na rodada, em 16 casos as duas transcrições concordaram no lugar, no período, na população ou no denominador errado de um bloco de registros. A conferência de contexto pegou os 16, e todos foram corrigidos.
- **Totais e taxas impressos:** os adjudicadores confirmaram na página 10 problemas em totais impressos e 36 taxas impressas que não batem com as próprias partes (3 e 17 no piloto, 7 e 19 na rodada), com as duas transcrições concordando em toda célula envolvida: são erros da fonte, marcados em `source_inconsistency`. O status `differs` em `qa/totals_check.csv` (67) e em `qa/rates_check.csv` (200) é maior que isso porque o conferidor ainda pareia algumas partes errado (tabela em duas páginas, linha de porcentagem somada como parte, total de coluna tomado como denominador); leia a `note` e o `source_inconsistency` do registro antes de tratar um caso como erro.
- **Limites conhecidos:**
  - Células pequenas: há contagens de 1 e 2 em tabelas por idade, sexo e mês (ferraroni1979, rodriguez1984, araujofilho1980, koifman1974, moraes1989), e um registro de texto de araujofilho1980 sobre um único paciente. São dados agregados e ficaram; nenhum deles se combina com outra coisa nos arquivos que aponte para uma pessoa.
  - Unidades e períodos ficam como impressos, sem data ISO e sem valor convertido: "%", "por 100" e "por cem mil habitantes" convivem.
  - O tamanho de amostra de um inquérito fica no estrato do estudo e não desce.
  - Os 28 são artigos de periódico. Ainda não há boletim oficial, nem dado dos anos 1990: a coleta mais recente é de 1989 (santos1995). O Informe Epidemiológico do SUS (1992-94) e a bvsms não responderam.
  - A conferência de disponibilidade tem lacunas: não deu para ler o início online do SISPCE (esquistossomose), e alguns servidores do SciELO e da Fiocruz recusaram acesso por script.

## Licença e citação

- O dataset (os arquivos CSV, o schema e os scripts) é publicado sob a licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Por favor, cite as publicações originais listadas em `data/sources.csv` e também este dataset. Cada linha também traz a sua fonte em `citation` e a situação de licença da fonte em `license`.
- As publicações não são redistribuídas. A maioria é CC BY-NC 4.0 na página do artigo no SciELO; galvao1985, moraes1989 e ferraroni1979 são CC BY 4.0 na página do artigo; camargo1984 e baruffa1974 ficam sob o CC BY 4.0 da Revista do Instituto de Medicina Tropical de São Paulo inteira, e giugliano1977 sob o da Acta Amazonica, sem licença no item; a licença de certain1972 não foi confirmada. Nenhum PDF imprime licença, porque todos são escaneamentos das edições impressas. Aqui são usados só contagens, taxas e médias, que são fatos, e citações curtas de no máximo 15 palavras.

Erros ou registros que faltam: por favor, [abra uma issue](https://github.com/paper-rerun/public-health-historical-br/issues).

## Como este dataset foi feito

Este dataset foi montado por agentes de IA (Claude, da Anthropic) num computador doméstico e revisado por uma pessoa antes da publicação. Nenhum valor foi estimado ou digitado à mão: cada um foi transcrito do PDF original duas vezes, de forma independente, e cada divergência foi conferida na página. O método e os scripts estão em `method/`. Como funciona o projeto como um todo (em inglês): https://github.com/paper-rerun/paper-rerun/blob/main/METHOD.md

Contato: Filipe Tessaro, pelas issues deste repositório.
