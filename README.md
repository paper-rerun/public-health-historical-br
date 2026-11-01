# Historical public health data from Brazil, 1960-1989

Versão em português: [README.pt-BR.md](README.pt-BR.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23680401.svg)](https://doi.org/10.5281/zenodo.23680401)

7,467 records taken from the tables, figures and text of 28 articles printed in Portuguese between 1968 and 1995, on data collected from 1960 to 1989. They cover Chagas disease, schistosomiasis, filariasis, cysticercosis, hepatitis B, malaria, leprosy, tuberculin tests, meningitis, tetanus, measles, infant and maternal mortality, mortality by cause, child diarrhoea, nutrition, dental caries, hypertension and vaccine coverage, from Amazonas to Rio Grande do Sul. Each row is one printed cell or one number of the text, with the page and table it came from.

None of these numbers exists in structured form at that period or level of detail. The official health series that are online start after most of these studies: mortality (SIM) in 1979, the SINAN notification series for leprosy, tuberculosis and acute Chagas disease in 2001, vaccine coverage (SI-PNI) in 1994, malaria by state in 1990 and child nutrition (SISVAN) in 2008, and no series holds serology, skin tests or hospital records. Each document was checked against the relevant series and against DataCite and Harvard Dataverse before it was transcribed; the result for each one is in `availability_check` of `data/sources.csv`.

The data are aggregated: counts, rates, percentages and means by place, age group, sex and year. Tables that list individuals are skipped and nothing of them is in the files (one table in the pilot, none in the round). No file has a name of a patient, an address or a date of birth.

Part of [Paper Rerun](https://paper-rerun.github.io), in its Open Tables line. The work was done by AI agents on a home computer and reviewed by a human before publication.

## Versions

- **v2.0.0** (November 2026): 28 articles. Adds a round of 20 articles to the 8 of the pilot, with schema 2.0: a fixed rule for `measure_as_printed`, the denominator and unit taken from the caption and methods, `total_kind` = `overall` for the rate or mean of the whole group, and a check for long copies run by each adjudicator. The pilot files are unchanged.
- **v1.0.0** (October 2026): pilot of 8 articles, 2,619 records.

## What is in it

| | |
|---|---|
| Publications | 28 journal articles printed 1968 to 1995: Revista de Saúde Pública, Revista da Sociedade Brasileira de Medicina Tropical, Cadernos de Saúde Pública, the journals of the São Paulo State Health Department, Revista do Instituto de Medicina Tropical de São Paulo and Acta Amazonica |
| Strata | 901: 28 studies, 312 places, 267 age groups, 179 population groups, 57 sex strata, 45 data sources and 13 other |
| Records | 7,467: persons in a class 1,380, cases 1,166, prevalence 865, persons examined 639, mortality rate 377, positive results 374, incidence rate 359, deaths 339, detection rate 302, population 278 and others. 1,331 of them are printed totals |
| Statistics | count 3,693, rate or proportion 2,015, percentage share 1,309, mean 212, dispersion 95, median 52, ratio 43, other 48. Rates: 2,248 per 100, 764 per 100,000, 173 per 10,000 and 114 per 1,000 |
| Where they came from | the study's own survey 3,535, hospital or facility records 1,249, notifications 950, control programmes 619, vital records 396, cited publications 282, mixed 257, population estimates 107, not stated 72 |

| Document | What it is | Place | Strata | Records |
|---|---|---|---:|---:|
| camargo1984 | national rural serosurvey of Chagas infection, 1975-80 | Brazil | 32 | 99 |
| albuquerque1989 | leprosy detection rate by sex, age and clinical form, 1960-85 | Recife, PE | 16 | 421 |
| ferreira1988 | nutritional status of children under 5, 1985 | RO | 16 | 168 |
| rodriguez1984 | measles serology and vaccine coverage at 7 health posts, 1983 | Curitiba and São José dos Pinhais, PR | 32 | 315 |
| certain1972 | tuberculin test of first-year pupils in 104 state schools, 1970 | São Paulo, SP | 13 | 416 |
| pereira1980 | mortality by cause, sex and age, 1977-78 | DF | 16 | 112 |
| ferraroni1979 | malaria in two hospitals, 1974-77 | Manaus, AM | 41 | 653 |
| coura1987 | schistosomiasis prevalence in 47 municipalities, 1978-85 | PB | 61 | 435 |
| costa1980 | schistosomiasis in workers of nine sugar plantations, 1977 | Catende, PE | 21 | 169 |
| araujo1973 | infant mortality and causes, with water connections, 1960-69 | Salvador and inland Bahia, BA | 8 | 82 |
| souza1983 | maternal mortality in the maternity hospitals, 1975-79 | Florianópolis, SC | 15 | 185 |
| souza1969 | dental caries (DMF-T) of schoolchildren aged 7 to 12, 1968 | Brasília, DF | 14 | 200 |
| iversson1976 | meningococcal disease by month, district, age and sex, 1968-74 | São Paulo, SP | 41 | 684 |
| campos1995 | diarrhoea and deaths in children under 5, household surveys of 1986 and 1989 | São Luís, MA | 42 | 269 |
| santos1995 | weight and height deficits of preschool children in 7 municipalities, 1989 | semi-arid Bahia, BA | 19 | 114 |
| koifman1974 | tetanus cases, deaths, rates and lethality, 1960-69 | Guanabara, RJ | 74 | 398 |
| correialima1976 | Chagas serology in 24 municipalities, 1975 | PI | 48 | 271 |
| menezes1980 | schistosomiasis by stool test and skin test, with snails, 1974 | Riachuelo, SE | 27 | 371 |
| araujofilho1980 | measles outbreak, attack rates by locality and age, 1976 | Ilha Grande, RJ | 43 | 241 |
| dobbin1968 | bancroftian filariasis by age and sex, and Culex infection, 1963 | São Lourenço da Mata, PE | 10 | 46 |
| alecrim1986 | HBsAg by age in people with and without clinical hepatitis | Lábrea, AM | 13 | 52 |
| vianna1986 | cysticercosis serology in serum and cerebrospinal fluid | Brasília, DF | 108 | 299 |
| galvao1985 | leprosy prevalence, incidence and new cases by form and municipality, 1972-84 | Presidente Prudente region, SP | 54 | 502 |
| moraes1989 | Haemophilus meningitis confirmed by culture, 1960-77 | São Paulo, SP | 75 | 372 |
| szwarcwald1985 | vaccine coverage of children aged 12 to 23 months, 1983 | Teresina, PI | 14 | 102 |
| klein1985 | hypertension prevalence in adults and cardiovascular mortality, 1979 | Volta Redonda, RJ | 22 | 258 |
| baruffa1974 | Chagas serology of 1,383 people in five municipalities, 1970-71 | southern Rio Grande do Sul, RS | 19 | 93 |
| giugliano1977 | nutritional status and clinical signs of preschool children of a day care centre, 1976 | Manaus, AM | 7 | 140 |

Files:
- `data/records.csv`: one record per row (7,467), with `doc_id`, `page` and `table_or_figure`. Each record carries its own effective values (period, unit, rate base, condition, measure), plus the column header, the table label and kind, the period, unit, rate base, case definition and classification printed for the table, its "Fonte:" lines and the meaning of the footnote.
- `data/strata.csv`: one stratum per row (901). Strata nest through `parentStratumID`, from the study down to places, age groups, sex, population groups and data sources. A context field the child stratum does not print is taken from the nearest parent that prints it, and `inherited` says from which; label, sample size, pages and notes are never passed down.
- `data/sources.csv`: the 28 publications, with authors, record link, licence notice and the availability check.
- `qa/decisions.csv`: every disagreement between the two independent transcriptions and how it was settled against the PDF (11,554 decisions, with page).
- `qa/totals_check.csv`: each printed total against the sum of its transcribed parts (1,105 checks). It is a check, not data; the dataset does not change with it.
- `qa/rates_check.csv`: each rate or percentage printed next to its count, against numerator / denominator (1,400 checks). Also a check, not data.
- `method/`: the schema (`schema.json`, built by `build_schema.py`), its self-check, the comparison and merge scripts and the long-copy check. They run in the working folder, with the transcriptions and the PDFs, which are not included here.

### Columns

All files join `data/sources.csv` on `doc_id`. Records join strata on `doc_id` and `stratum_ids`: `stratum_ids` lists the strata of the record within its document ("s30; s65; s3"), and `stratumID` is `doc_id#s30`. A record belongs to all the strata it lists, such as a municipality, an age group and a sex; `stratum_labels` and `stratum_dimensions` repeat their labels and kinds in the same order. In `qa/totals_check.csv`, `record_id` is the total, and `part_record_ids` lists the parts that were summed. In `qa/rates_check.csv`, `record_id` is the rate, and `numerator_record_id` and `denominator_record_id` are the records it was recomputed from. `decision_ids` in a record lists the `diff_id` of its rows in `qa/decisions.csv`, within the same `doc_id`.

Labels, periods, conditions and units are kept exactly as printed. A misprint of the source stays, and when it was confirmed on the page the record says so in `source_inconsistency` (117 records). Printed totals are kept as records with `is_total` = True and are never recomputed; `total_kind` says if a total is a row, column, grand total, subtotal or `overall`, the rate or mean of the whole group (226), which is not a sum. Numbers an article cites from another study are kept with `data_source_kind` = `cited_publication` (282 records), so one filter takes them out.

The main columns:
- `record_id`: the record, as `doc_id#0001`. `page` is the PDF page counted from 1; `table_or_figure` is the label as printed ("TABELA 6", "Gráfico 3"), or `text` for a number in the text.
- `period_as_printed` and `period_context_as_printed`: the period of the record as printed and the wider period of the caption or methods.
- `condition_as_printed`: the disease, infection or class the number is about, as printed.
- `measure_standardized` and `measure_as_printed`: what was counted or measured, in our list of terms (`prevalence`, `cases`, `incidence_rate`, `persons_examined` and others in `method/schema.json`) and in the words of the source.
- `value`, `value_as_printed` and `value_kind`: the number ready for calculation, with a decimal point, and the cell as printed. 7,382 values are numeric; 40 are illegible and keep the best reading, 12 are malformed in print, 18 are classes, 7 are symbols and 8 are ranges, with `value_min` and `value_max`.
- `unit_as_printed`, `rate_multiplier` and `rate_denominator_as_printed`: the unit as printed, the base of a rate as a number (100, 1000, 10000, 100000) and the population the rate is taken over, as printed.
- `statistic`: `count`, `rate_or_proportion`, `percentage_share`, `cumulative_percentage`, `mean`, `median`, `dispersion_measure`, `ratio`, `geometric_mean` or `other`.
- `data_source_kind`: where the number comes from. `is_estimate` marks the 120 numbers the source prints as estimates.
- `origin` and `decision_ids`: whether the final record is the one both transcriptions agreed on (2,946), the one of transcription A (1,330) or B (1,840), or a corrected one (1,351), and the decisions behind it.

## How it was made

1. **Collection.** Agents harvested the Revista de Saúde Pública and the journals of the São Paulo State Health Department through OAI-PMH, read the SciELO tables of contents of the Revista da Sociedade Brasileira de Medicina Tropical, Cadernos de Saúde Pública and other journals, and searched for state bulletins, SUCAM/FUNASA and Ministry of Health material. Every candidate left out is recorded with the reason.
2. **Availability check.** Only documents whose numbers do not exist in structured form at that period or level of detail were taken. The start year of each official series was read in the series itself (the period lists of the TabNet forms, the SIDRA API), and each document went through searches in DataCite (which registers Zenodo, figshare, Dryad, SciELO Data and Mendeley Data DOIs) and Harvard Dataverse.
3. **Two independent transcriptions.** Two agents per article transcribed the strata, an inventory of the tables, figures and text blocks with numbers, and every data cell into a fixed schema, without seeing each other's work, copying labels, periods, units and numbers exactly as printed. Lists of individual cases were inventoried with 0 cells and not transcribed.
4. **Comparison and adjudication.** A script paired the two transcriptions stratum by stratum and record by record and listed every disagreement and every entry present in only one of them. Each one was settled by checking the rendered page, with the page as evidence. In the round, each document also got a separate pass that checked place, period, population, case definition, denominator, unit and rate base of each table on its own, to catch context errors that both transcriptions make together.
5. **Merge and checks.** A script merged the adjudicated documents, filled each stratum from its parent, summed the parts of each printed total and recomputed each rate printed next to its count. Records are written as adjudicated, with no inheritance. Long copies of the source and dates, addresses and birth dates are searched in every cell: 0 long copies; the only hits for "rua" (street) are a class of rubbish disposal in campos1995. Nothing in the dataset was changed by the totals and rates checks.

## How accurate it is

- **Numbers:** across the 7,422 paired records of both rounds, one digit was misread once, in the round (costa1980 TABELA 2, 24 read as 21), and corrected. The other value fields decided against one side are copying rules, such as a separator normalised or "nenhum" written as 0.
- **Fields:** in the round, transcription A had 98.69% of its fields right and B 98.46% (98.44% and 99.17% in the pilot).
- **Whole records:** counting the records each one left out, A alone was fully correct on 61.4% of the round's records and B on 66.1% (57.1% and 71.4% in the pilot). The gap from the per-field numbers comes from context cascades: a record counts as wrong if any of its fields is wrong, and most errors were one rule misread across a whole document, such as the condition or the row label, which puts the same wrong field in every row of a table. All 11,554 disagreements were settled against the PDF, so the final data do not depend on either transcription alone.
- **Context errors:** in the round, 16 cases had both transcriptions agree on the wrong place, period, population or denominator for a block of records. The context pass caught them and they were fixed.
- **Printed totals and rates:** the adjudicators confirmed on the page 10 problems in printed totals and 36 printed rates that do not match their own parts (3 and 17 in the pilot, 7 and 19 in the round), with both transcriptions agreeing on every cell involved: they are errors of the source, flagged in `source_inconsistency`. The `differs` status in `qa/totals_check.csv` (67) and `qa/rates_check.csv` (200) is higher than that because the checker still pairs some parts wrongly (tables over two pages, a percentage row summed as a part, a column total taken as denominator); read the `note` and the record's `source_inconsistency` before treating one as an error.
- **Known limits:**
  - Small cells: some counts of 1 or 2 in tables by age, sex and month (ferraroni1979, rodriguez1984, araujofilho1980, koifman1974, moraes1989), and one text record of araujofilho1980 about a single patient. They are aggregated data and were kept; none of them combines with anything else in the files that would point to a person.
  - Units and periods are as printed, with no ISO dates and no converted values: "%", "por 100" and "por cem mil habitantes" stand side by side.
  - The sample size of a survey stays in the study stratum and is not passed down.
  - All 28 are journal articles. There is no official bulletin yet, and no data from the 1990s: the latest collection is 1989 (santos1995). The Informe Epidemiológico do SUS (1992-94) and bvsms could not be reached.
  - The availability check has gaps: the online start of SISPCE (schistosomiasis) could not be read, and some SciELO and Fiocruz servers refused scripted access.

## Licence and citation

- The dataset (the CSV files, schema and scripts) is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please cite the original publications listed in `data/sources.csv` as well as this dataset. Each row also carries its source in `citation` and the licence situation of its source in `license` (in Portuguese).
- The publications are not redistributed. Most are CC BY-NC 4.0 on their SciELO article pages; galvao1985, moraes1989 and ferraroni1979 are CC BY 4.0 on their article pages; camargo1984 and baruffa1974 fall under the CC BY 4.0 of the whole Revista do Instituto de Medicina Tropical de São Paulo, and giugliano1977 under that of Acta Amazonica, with no licence on the item; the licence of certain1972 is not confirmed. No PDF prints a licence, since all are scans of the printed issues. Only counts, rates and means, which are facts, and short citations of at most 15 words are used here.

Errors or missing records: please [open an issue](https://github.com/paper-rerun/public-health-historical-br/issues).

## How this dataset was made

This dataset was built by AI agents (Claude, by Anthropic) on a home computer and reviewed by a human before publication. No value was estimated or typed by hand: each one was transcribed from the source PDF twice, independently, and every disagreement was checked against the page. The method and scripts are in `method/`. How the wider project works: https://github.com/paper-rerun/paper-rerun/blob/main/METHOD.md

Contact: Filipe Tessaro, via issues on this repository.
