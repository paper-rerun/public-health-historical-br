# Historical public health data from Brazil, 1960-1985

Versão em português: [README.pt-BR.md](README.pt-BR.md)

2,619 records taken from the tables, figures and text of 8 articles printed in Portuguese between 1972 and 1989, one per disease or indicator: a national serosurvey of Chagas disease in 1975-80, leprosy detection in Recife from 1960 to 1985 (PE), the nutritional status of children under 5 in 3 municipalities of Rondônia in 1985 (RO), measles immunity and vaccine coverage of children aged 5 to 15 months in Curitiba and São José dos Pinhais in 1983 (PR), a tuberculin survey of first-year schoolchildren in São Paulo in 1970 (SP), mortality by cause in the Distrito Federal in 1977-78 (DF), malaria in two hospitals of Manaus in 1974-77 (AM) and the schistosomiasis control programme in Paraíba in 1978-85 (PB). Each row is one printed cell or one number of the text, with the page and table it came from.

None of these numbers exists in structured form. The official health series that are online start after these studies: mortality (SIM) in 1979, the SINAN notification series for leprosy, tuberculosis and acute Chagas disease in 2001, vaccine coverage (SI-PNI) in 1994, malaria by state in 1990 and child nutrition (SISVAN) in 2008. No series holds serology, tuberculin tests or hospital records at all. Each document was checked against the relevant series and against DataCite and Harvard Dataverse before it was transcribed, and the result for each one is in the table below.

The data are aggregated: counts, rates, percentages and means by place, age group, sex and year. One table of ferraroni1979 lists each malaria death in a row (TABELA 5, p9); it was skipped and nothing of it is in the files. No file has a name of a patient, an address or a date of birth.

Part of [Paper Rerun](https://paper-rerun.github.io), in its Open Tables line. The work was done by AI agents on a home computer and reviewed by a human before publication.

## What is in it

| | |
|---|---|
| Publications | 8 journal articles printed 1972 to 1989: 5 in Revista de Saúde Pública, 1 in Revista do Instituto de Medicina Tropical de São Paulo, 1 in Acta Amazonica and 1 in Revista da Sociedade Brasileira de Medicina Tropical. By kind of data: 4 surveys, 1 notification series, 1 of vital statistics, 1 of hospital records and 1 of a control programme |
| Strata | 227: 8 studies, 96 places (municipalities, states, regions, 2 hospitals and 1 school), 72 age groups, 15 sex strata, 14 population groups, 13 data sources and 9 other (the age at vaccination in rodriguez1984) |
| Records | 2,619: persons in a class 832, prevalence 490, detection rate 302, hospital days 180, cases 157, persons examined 98, sample units 80, proportional mortality 64, protected 60, hospital admissions 59, time interval 54, other measures 143. 522 of them are printed totals |
| Statistics | count 1,256, rate or proportion 777, percentage share 431, mean 66, median 47, dispersion 26, ratio 14, geometric mean 2. Rates: 830 per 100, 320 per 100,000 and 3 per 1,000 |
| Where they came from | 2,516 records from tables, 84 from the text or a note and 19 from figures that print their values. 38 are estimates, and 27 are numbers of another study cited by ferreira1988 |

| Document | What it is | Place | Period, as printed | Strata | Records | Availability check |
|---|---|---|---|---:|---:|---|
| camargo1984 | national rural serosurvey of Chagas infection, SUCAM and CNPq; prevalence estimate by state | Brazil | 1975/1980 | 32 | 99 | no official series has Chagas serology, and SINAN (from 2001) has acute cases only; WHO and PAHO give one estimate per country; 0, 2 and 16 hits in DataCite and Dataverse, all recent. The same survey was printed again by state and municipality in 2011, also as PDF tables |
| albuquerque1989 | leprosy detection rate in Recife by sex, age and clinical form, from the files of the Health Department | Recife, PE | entre 1960 e 1985 | 16 | 421 | SINAN leprosy starts in 2001, and there is nothing by municipality before it; 0, 2 and 11 hits, all from 2000 on |
| ferreira1988 | nutritional status of children under 5 in 3 municipalities of the Polonoroeste programme, compared with ENDEF and Jauru | RO | 1985 | 16 | 168 | SISVAN starts in 2008 and the POF anthropometry on SIDRA in 2002-03; the PNSN 1989 microdata (ICPSR 2294) are another survey and did not sample these municipalities |
| rodriguez1984 | measles serology and vaccine coverage of children aged 5 to 15 months at 7 health posts | Curitiba and São José dos Pinhais, PR | entre os meses de junho e outubro de 1983 | 32 | 315 | SI-PNI starts in 1994, and measles serology is in no series; 0 hits |
| certain1972 | tuberculin test of first-year pupils in 104 state schools, by age, sex and induration; tables printed rotated | São Paulo, SP | 1970 | 13 | 416 | SINAN tuberculosis starts in 2001 and holds notified cases, never tuberculin tests; 0 hits |
| pereira1980 | proportional mortality and death rates by cause, sex and age, residents of the DF | DF | 1977 e 1978 | 16 | 112 | SIM starts in 1979 and the Civil Registry on SIDRA in 2003, so 1977-78 is outside both; the printed 1977 national mortality volume was not found online |
| ferraroni1979 | malaria at the Hospital de Moléstias Tropicais and the Hospital Geral de Manaus: cases, days in hospital, parasitaemia | Manaus, AM | abril de 1974 a dezembro de 1977 | 41 | 653 | hospital data never entered an official series; malaria by state starts in 1990 (SISMAL 1996, SIVEP-Malária 2003) |
| coura1987 | schistosomiasis prevalence in 47 municipalities, from the SUCAM evaluations of the control programme (PECE) and the authors' own 1984/85 sample | PB | de 1978 a 1983 e posteriormente em 1984/85 | 61 | 435 | nothing by municipality for 1978-85 in DATASUS, SIDRA or dados.gov.br; 0 hits. The start year of the online SISPCE series could not be read, so this check has a gap |

Files:
- `data/records.csv`: one record per row (2,619), with `doc_id`, `page` and `table_or_figure`. Each record carries its own effective values (period, unit, rate base, condition, measure), plus the column header, the table label and kind, the period, unit, rate base, case definition and classification printed for the table, its "Fonte:" lines and the meaning of the footnote.
- `data/strata.csv`: one stratum per row (227). Strata nest through `parentStratumID`, from the study down to places, age groups, sex, population groups and data sources. A context field the child stratum does not print (place above, period, population, data source, case definition, method) is taken from the nearest parent that prints it, and `inherited` says from which; label, sample size, pages and notes are never passed down.
- `data/sources.csv`: the 8 publications, with authors, record link and licence notice.
- `qa/decisions.csv`: every disagreement between the two independent transcriptions and how it was settled against the PDF (5,925 decisions, with page).
- `qa/totals_check.csv`: each printed total against the sum of its transcribed parts (522 totals). It is a check, not data; the dataset does not change with it.
- `qa/rates_check.csv`: each rate or percentage printed next to its count, against numerator / denominator (352 rates). Also a check, not data.
- `method/`: the schema, the comparison script and the merge script. They run in the working folder of the pilot, with the transcriptions and the PDFs, which are not included here.

### Columns

All files join `data/sources.csv` on `doc_id`. Records join strata on `doc_id` and `stratum_ids`: `stratum_ids` lists the strata of the record within its document ("s30; s65; s3"), and `stratumID` is `doc_id#s30`. A record belongs to all the strata it lists, such as a municipality, an age group and a sex; `stratum_labels` and `stratum_dimensions` repeat their labels and kinds in the same order. In `qa/totals_check.csv`, `record_id` is the total in `data/records.csv`, and `part_record_ids` lists the numbers after the `#` of the parts that were summed. In `qa/rates_check.csv`, `record_id` is the rate, and `numerator_record_id` and `denominator_record_id` are the records it was recomputed from. `decision_ids` in a record lists the `diff_id` of its rows in `qa/decisions.csv`, within the same `doc_id`.

Labels, periods, conditions and units are kept exactly as printed. A misprint of the source stays, and when it was confirmed on the page the record says so in `source_inconsistency` (33 records). Printed totals are kept as records with `is_total` = True and are never recomputed; `total_kind` says if a total is a row, column, grand total or subtotal. 86 of the 522 are not sums: they are the rate, mean or percentage of the whole group, such as the "Total" row of a prevalence column. Numbers that ferreira1988 cites from ENDEF 1974-75 are kept with `data_source_kind` = `cited_publication` (27 records), so one filter takes them out.

### Main columns

The files are UTF-8, with commas between columns. In every record, `doc_id` links the row to `data/sources.csv`, and `page` and `table_or_figure` say where it came from (PDF page counted from 1, and the label as printed, "TABELA 6", "Gráfico 3", or `text` for a number in the text). `record_id` is the record, as `doc_id#0001`.

- `stratum_ids`: the strata the record belongs to.
- `stratumID`, `parentStratumID` and `stratum_dimension`: the stratum, the stratum above it and its kind (`study`, `place`, `age_group`, `sex`, `population_group`, `data_source`, `other`).
- `period_as_printed` and `period_context_as_printed`: the period of the record as printed ("1977", "junho a outubro de 1983") and the wider period of the caption or methods ("entre 1960 e 1985"). 2,584 records have a period and 1,339 also have a context period.
- `condition_as_printed`: the disease, infection or class the number is about, as printed ("hanseníase", "infecção pelo S. mansoni", "vivax").
- `measure_standardized` and `measure_as_printed`: what was counted or measured, in our list of terms (`prevalence`, `detection_rate`, `persons_examined`, `hospital_days`, `proportional_mortality` and others in `method/schema.json`) and in the words of the source. `measure_as_printed` has no fixed rule yet (see the limits); use `measure_standardized` to group records.
- `value`, `value_as_printed` and `value_kind`: the number ready for calculation, with a decimal point, and the cell as printed ("2.631", "5,5"). 2,609 values are numeric; 5 are illegible and keep the best reading, 2 are malformed in print ("100 0", "0 9"), 2 are words ("nenhum", "um") and 1 is a range, with `value_min` and `value_max`.
- `unit_as_printed`, `rate_multiplier` and `rate_denominator_as_printed`: the unit as printed ("%", "por cem mil habitantes", "dias"), the base of a rate as a number (100, 1000, 100000) and the population the rate is taken over, as printed.
- `statistic`: `count`, `rate_or_proportion`, `percentage_share`, `mean`, `median`, `dispersion_measure`, `ratio` or `geometric_mean`.
- `is_total` and `total_kind`: whether the record is a printed total, and of which kind.
- `data_source_kind`: where the number comes from: the study's own survey (1,085 records), hospital records (647), notifications (413), a control programme (321), vital records (102), a cited publication (27), a population estimate (13) or not stated (11). `is_estimate` marks the 38 numbers the source prints as estimates.
- `origin` and `decision_ids`: whether the final record is the one both transcriptions agreed on (1,233), the one of transcription A (265) or B (636), or a corrected one (485), and the decisions behind it.
- `inherited` (strata): the fields the stratum took from a parent, and from which ("period_as_printed:s1").

## How it was made

1. **Collection.** An agent harvested the Revista de Saúde Pública through OAI-PMH (5,271 records) and, in part, the journals of the São Paulo State Health Department (6,495 records, stopped before the end), read the SciELO tables of contents of the Revista da Sociedade Brasileira de Medicina Tropical from 1967 to 1999, and searched the web for state bulletins, SUCAM/FUNASA, Fiocruz and Acta Amazonica. 26 candidates were read and left out, each with the reason: 13 good documents kept for the full round to balance disease, region and source, 7 whose content does not fit (statistical tests, case reports, reviews, short notes), 3 offline when we tried, 2 already structured (SB Brasil 1986 as xlsx on the Ministry site, PNSN 1989 at ICPSR) and 1 that prints again a chosen survey.
2. **Availability check.** Only documents whose data do not exist in structured form were taken. The start year of each official series was read in the series itself (the period lists of the TabNet forms, the SIDRA API), and each document went through three searches in DataCite (which registers Zenodo, figshare, Dryad, SciELO Data and Mendeley Data DOIs) and Harvard Dataverse.

   | Official series | Online since |
   |---|---|
   | SIM, mortality (TabNet, ICD-9) | 1979 (ICD-10 from 1996) |
   | SINAN tuberculosis | 2001 |
   | SINAN leprosy | 2001 |
   | SINAN acute Chagas disease | 2001; never serology |
   | SI-PNI, vaccine coverage | 1994 |
   | IBGE SIDRA, Civil Registry (deaths and live births) | 2003 |
   | Malaria by state (IDB/RIPSA) | 1990; SISMAL 1996, SIVEP-Malária 2003 |
   | SISVAN, nutrition | 2008 |
   | POF anthropometry on SIDRA | 2002-03 |
   | SISPCE, schistosomiasis | not verified: none of the three DEF paths returned a form |

3. **Two independent transcriptions.** Two agents per article transcribed the strata, an inventory of the tables, figures and text blocks with numbers, and every data cell into a fixed schema, without seeing each other's work, copying labels, periods, units and numbers exactly as printed. Lists of individual cases were inventoried with 0 cells and not transcribed; both agents did that for ferraroni1979 TABELA 5.
4. **Comparison and adjudication.** A script paired the two transcriptions stratum by stratum and record by record and listed every disagreement and every entry present in only one of them. Each one was settled by checking the rendered page, with the page as evidence. The adjudicators paired again by hand 78 one-sided rows that were the same record split differently by A and B.
5. **Merge and checks.** A script merged the adjudicated documents, filled each stratum from its parent, summed the parts of each printed total and recomputed each rate printed next to its count. Records are written as adjudicated, with no inheritance. The same script looks for any cell that copies more than 15 words of the source and for dates, addresses and birth dates in every cell. It found one copied label of 17 words in rodriguez1984 p7, which was replaced by the other transcription's label of 12 words; after that, 0. Nothing in the dataset was changed by the totals and rates checks.

## How accurate it is

- **Numbers:** no digit was misread in either transcription. In the 2,619 paired records, 10 value fields were decided against one side, and none of them is a misreading: they are copying rules, such as "0.34" printed with a point among commas and written "0,34", or the words "nenhum" and "um" written as 0 and 1. The hard cases passed: the OCR text layer of camargo1984, which reads "2.t9" where the page prints a number, the rotated tables of certain1972, a count and a percentage in one cell, "20 (11,5)", and the numbers of ferraroni1979 that print too faint to read for sure (7 decisions), kept as illegible with the best reading. One word was misread in a label, in a note of ferraroni1979 TABELA 4.
- **Fields:** 35 fields were compared in each record. Transcription A had 1,432 of 91,665 wrong, 98.44% right; transcription B had 765 wrong, 99.17% right.
- **Whole records:** A alone was fully correct on 57.1% of records and B on 71.4%, counting the records each left out (3 and 1). The gap from the per-field numbers comes from context cascades. A record counts as wrong if any of its 35 fields is wrong, and most errors were one rule misread across a whole document, which puts the same wrong field in every row of a table. B put the whole-study stratum on all 99 cells of camargo1984, whose rows each print a state; A left the rate denominator empty in 330 records of coura1987; B left the unit "crianças" empty in 324 records of rodriguez1984. So the same side scores 96.0% on one document and 0.0% on another, and a side that reads the rule right passes 92% on almost every document. Counting only content fields (value, label, condition, measure, statistic, period, unit, total), 88.2% of A's records and 88.6% of B's were right. Strata: 78.4% and 86.8%. Tables: 54.7% and 60.0%. All 5,925 disagreements were settled against the PDF, so the final data do not depend on either transcription alone.
- **Printed totals:** of the 522 totals, 420 can be checked against their parts: 407 add up exactly, 6 add up within rounding and 7 do not add up. The other 102 are 86 that are not sums (the rate or mean of the whole), 8 in figures that print only some bars and 8 with an illegible or malformed part. The 6 within rounding are 4 percentage columns of ferreira1988 that add up to 99.9 and 2 counts of ferraroni1979 off by 1. The two transcriptions agree on every cell involved in the 7, and each case was opened on the page: they are 3 errors of the source. Each case is in `qa/totals_check.csv`, in `status` and `note`.
  - ferraroni1979 TABELA 4, venereal diseases: Military 99 + Civil 3 make 102; the Total column prints 112. With 112 the Total column adds up to 354, and the printed TOTAL is 344, which is Military (285) + Civil (59). The 112 is the error. 2 rows.
  - ferraroni1979 TABELA 6, 1976 totals: the row "02** — 04" prints 17 in the ±± total, where vivax 18 + falciparum 9 make 27; the row "30 — 39" prints 15 in the ± total, where 31 + 34 make 65. The column totals (391 and 377) add up with 65 and 27, so the authors summed right and the two cells were misprinted. 4 rows.
  - ferreira1988 TABELA 2, Ouro Preto D'Oeste: the percentage column adds up to 100.8. Eutrofia prints 87.8, and 335 / 385 is 87.0. 1 row.
- **Rates against their counts:** 352 rates or percentages print their count next to them. 322 match it (298 within rounding and 24 where the author cut the last digit instead of rounding, such as 82.0 printed for 32 / 39 = 82.05 in rodriguez1984), 13 are one last digit off and 17 do not match. Another 816 rates print no numerator in the table (prevalence estimates, coefficients per 100,000 with no population) and were not checked. Do not use the percentages of the 1970-77 block of albuquerque1989 TABELA 6 or the female vivax percentages of 1976 in ferraroni1979 TABELA 1 as they are; the counts of those tables are right. Each case is in `qa/rates_check.csv`, in `status`.
  - albuquerque1989 TABELA 6, 1970-77 block (5): the percentages add up to 100.0 and the counts to 738, but one is not the other: 32 / 738 is 4.3 and the page prints 4.7; 268 gives 36.3 against 39.0; 322 gives 43.6 against 39.4. The 1978-85 and 1970-85 blocks match.
  - ferraroni1979 TABELA 4 (3): the percentages look computed over about 347 patients, not the 344 printed (60 / 344 is 17.4, printed 17.3), and the one of venereal diseases uses the 112 above.
  - ferraroni1979 TABELA 1, female vivax in 1976 (2): 78 and 27 over 105 give 74 and 26; the page prints 71 and 29. The counts add up with the row totals (245 and 122), so the error is in the percentages.
  - certain1972 TABELA 3 (4): differences of 0.01 to 0.03, as if the authors had divided by 941 instead of the 943 printed.
  - rodriguez1984 Tabela 6 (2): the row "7º a 8º" prints 12 children examined, with 59 not protected and 61 protected. The text on p5 says 120 vaccinated children: the table lost a zero.
  - ferreira1988 TABELA 2 (1): the 87.8 above.
- **Known limits:**
  - ferraroni1979 holds 653 records, 25% of the dataset. Without it, the whole-record accuracy is 48.1% for A and 67.1% for B.
  - The schema still leaves too much room in the context fields, which is why whole-record accuracy is low. `measure_as_printed` has no fixed rule: one side took it from the column header, the other from the condition. `total_kind` does not separate a sum from the rate of the whole (the 86 above).
  - Units and periods are as printed, with no ISO dates and no converted values: "%", "por 100" and "por cem mil habitantes" stand side by side, and 927 records print no unit, mostly counts whose `measure_standardized` says what was counted.
  - Some cells are counts of 1 or 2 in tables by age, sex and month (ferraroni1979, rodriguez1984). They are aggregated data and were kept; none of them combines with anything else in the files that would point to a person.
  - The sample size of a survey stays in the study stratum and is not passed down: "1.626.745 amostras" in camargo1984 is the whole survey, not each state.
  - The availability check has gaps: the online start of SISPCE could not be read (coura1987), bvsms.saude.gov.br answered 503, scielo.iec.gov.br did not answer, scielosp.org answered 403 to scripted downloads, search.scielo.org asked for a robot challenge (not attempted) and the Fiocruz ARCA answered 404. The IBGE "Estatísticas do Século XX" were not opened table by table.
  - All 8 are journal articles, none from the 1990s, and 5 come from the Revista de Saúde Pública. There is no official bulletin yet; the best candidate, the Informe Epidemiológico do SUS of 1992-94, was offline.

This is a pilot of 8 documents, run to settle the schema. A larger round, of 20 documents, is planned.

## Licence and citation

- The dataset (the CSV files, schema and scripts) is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please cite the original publications listed in `data/sources.csv` as well as this dataset. Each row also carries its source in `citation` and the licence situation of its source in `license` (in Portuguese).
- The publications are not redistributed. ferraroni1979 (Acta Amazonica) is CC BY 4.0 on its SciELO article page. The Revista do Instituto de Medicina Tropical de São Paulo states CC BY 4.0 for all its content on its "about" page, with no licence on the item, which covers camargo1984. albuquerque1989, ferreira1988, rodriguez1984 and pereira1980 (Revista de Saúde Pública) and coura1987 (Revista da Sociedade Brasileira de Medicina Tropical) are CC BY-NC 4.0 on their SciELO article pages; the USP journal site shows only a copyright line for the same articles. The licence of certain1972 is not confirmed: its SciELO page answered 502 twice. No PDF prints a licence, since all are scans of the printed issues. Only counts, rates and means, which are facts, and short citations of at most 15 words are used here.

Errors or missing records: please [open an issue](https://github.com/paper-rerun/public-health-historical-br/issues).

## How this dataset was made

This dataset was built by AI agents (Claude, by Anthropic) on a home computer and reviewed by a human before publication. No value was estimated or typed by hand: each one was transcribed from the source PDF twice, independently, and every disagreement was checked against the page. The method and scripts are in `method/`. How the wider project works: https://github.com/paper-rerun/paper-rerun/blob/main/METHOD.md

Contact: Filipe Tessaro, via issues on this repository.
