# Build ../schema.json (public health, version 2.0, for the round of 20)
# Source of the schema: schema.json is generated from this file and never edited by hand. Starts from
# saude-piloto/schema.json (saude-1.0-pilot, written by hand) with the 13 changes of saude-piloto/RODADA.md
# ("O que mudar no schema antes da rodada de 20"); SCHEMA_2.md says what each one changed
# Usage: py -3.12 -I -X utf8 method/build_schema.py   (writes ../schema.json; then run check_schema.py)
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
# sources.json comes with the collection step; until then doc_id is checked by pattern only
SOURCES_PATH = ROOT / "sources.json"
DOC_IDS = [document["id"] for document in json.loads(SOURCES_PATH.read_text(encoding="utf-8"))["documents"]] if SOURCES_PATH.exists() else []
SCHEMA_VERSION = "2.0"


def text(description=None):
	if description is None:
		return {"type": ["string", "null"]}
	return {"description": description, "type": ["string", "null"]}


def enum(description, values, nullable=False):
	result = {"type": ["string", "null"], "enum": values + [None]} if nullable else {"type": "string", "enum": values}
	if description is not None:
		result = {"description": description, **result}
	return result


def obj(properties, description=None):
	result = {"type": "object", "additionalProperties": False, "required": list(properties), "properties": properties}
	if description is not None:
		result = {"description": description, **result}
	return result


PAGE = {"type": "integer", "minimum": 1}
COUNT = {"type": "integer", "minimum": 0}
TABLE_ID = {"type": "string", "pattern": "^k[0-9]+$"}
STRATUM_ID = {"type": "string", "pattern": "^s[0-9]+$"}
RECORD_ID = {"type": "string", "pattern": "^r[0-9]+$"}
COLUMN_ID = {"type": "string", "pattern": "^c[0-9]+$"}

DESCRIPTION = "Fixed output format for every blind transcriber of the public health rounds of Open Tables (version 2.0, after the pilot of 8 documents). Each document gives one JSON object {doc_id, transcriber, schema_version, document_kind, strata, tables, records, end_checklist}. strata[] holds who and where the numbers are about: the study, then each printed place, population group, age group, sex and data source, with its fields and pages. records[] holds one entry per printed data cell: the condition or indicator as printed, a measure from a closed list (cases, deaths, population, persons examined, positives, prevalence, incidence rate, detection rate, mortality rate, coverage, etc.), the value as printed and as a number, the unit and the rate base as printed (per 100, per 1.000, per 100.000), the statistic, the period, the strata the cell belongs to, and is_total for printed totals, which are kept and never recomputed. Every table, figure and text block that prints numbers is inventoried first with a closed cell count and its axes and labels. Tables that list individual people are inventoried and never transcribed. The transcription copies what is printed and never computes, converts, infers or matches. Carried over from saude-1.0-pilot and the rounds before it (see changes_from_previous for what 2.0 changed): inventory first, read from the rendered page, copy exactly as printed, illegible cells stay in, contradictions with both versions, page from the PDF, totals as records, 15-word limit on quotes and as-printed fields, two independent transcriptions with diff and adjudication. Source PDFs, record pages and the availability check of each document are in sources.json."
RULES = [
	"1 SCOPE. Inventory and transcribe every page of the document, unless sources.json gives extract_pages for it; then only those pages go to tables[] and records[], and the rest is read only to fill strata[] (methods, sample, case definition, data source, period).",
	"2 PRIVACY FIRST. Only aggregated counts and rates are transcribed. A table, list or text block whose rows are single people (one row per case, death, patient or child, even without names: month, age, sex, as in ferraroni1979 Tabela 5, p9) is inventoried with kind individual_case_list, data_cells = 0, privacy_skip = true and a note giving only how many rows it has; none of its contents is copied anywhere. Never write in any field a person's name (other than an author cited as a data source), address, street, house, date of birth or anything that identifies a person. A small count in an aggregated table (a cell with 1) is aggregated data and stays. collected_by and data source fields name institutions, never people.",
	"3 INVENTORY FIRST, EVERY TABLE AND FIGURE. Before writing any record, render every page in scope and list in tables[], in page order, every table, figure, map, chart and text block that prints this study's numbers, with table_id, page, label, kind and data_cells. Every figure and map is inventoried, with data_cells = 0 and kind figure_unlabeled when it prints no value. A table continued on the next page gets one entry per page. A block without its own number but with its own header (a second year stacked under the same caption, ferraroni1979 Tabela 1, p3: the 1977 block under the 1976 block) is its own entry. A note under a table that prints values not in the body (pereira1980 Tabela 1, p2: 'População estimada para 1º de julho: 977.791 (1977)') is its own entry, kind text, label 'Tabela 1, nota'. At the end each entry closes: data_cells = transcribed + skipped_cells, and transcribed = number of records with that table_id.",
	"4 TEXT BLOCKS, NARROW. Inventory a text block only when it prints numbers of this study's results that no table or labelled figure prints (counts, rates, prevalences, the period or place they refer to). Methods, sample sizes, discussion of other studies and references are not inventoried: sample sizes and methods go to strata[] fields. Each text entry has one implicit column, c1, header 'text'; row_index is the order of the number in the block, so A and B pair text records by the number, not by the line.",
	"5 READ FROM THE RENDERED PAGE. The printed page is the source. All 8 pilot PDFs are scans: in the Revista de Saúde Pública ones the tables are images with no text layer, and the OCR layers of the others misread digits (camargo1984 p9: the layer reads 'l�a', 'tb�', '2.t9' where the page prints numbers). certain1972 prints Tabelas 1 and 2 rotated 90 degrees (p3, p4): read them turned, and say so in the table notes. Render at 150 dpi; go up only for one unreadable character.",
	"6 STRATA FIRST: WHO AND WHERE. One strata[] entry for the whole study (s1, stratum_dimension = study), then one per printed level of every axis that says who or where the numbers are about: place (region, state, municipality, district, locality, school, plantation, hospital), population_group (escolares, trabalhadores de campo, crianças vacinadas, não vacinadas, renda 0 - 4 SM), age_group, sex, and data_source when the document puts numbers from different sources side by side (SUCAM programme records next to the authors' survey in coura1987; ENDEF and Jauru next to Rondônia in ferreira1988 Tabelas 4 and 5). A level printed under another of the same dimension points to it in parent_stratum_id (a municipality under its hydrographic region in coura1987 Tabela 1; a state under its region in camargo1984 Tabela I); every other level points to s1. One stratum per distinct printed label inside a dimension: 'Masc.' and 'Masculino' are two strata, both sex_standardized = male. A place or group of a cited study (NE, RJ, SP and Jauru next to Rondônia in ferreira1988 Tabelas 4 and 5) points in parent_stratum_id to the data_source stratum of that study, not to s1, and that source stratum carries the cited study's age group, population group, period, case definition and method, so the place inherits them and never the study's own (Rondônia's age range and growth standard). A field the cited place prints for itself goes on the place. Fix the strata before writing records.",
	"7 WHAT WAS COUNTED IS NOT A STRATUM. The disease, cause of death, clinical form, nutritional class, reaction class, antibody titre class, parasitaemia class or mode of detection goes to condition_as_printed on the record, never to strata[]. Closed examples: albuquerque1989 Tabela 4 'V', 'D', 'I', 'T' (clinical forms) are conditions, the age groups '0 - 14' and '≥ 15' are strata; ferreira1988 Tabela 1 'Desnutrição I' is a condition, 'Ariquemes' is a stratum; pereira1980 Tabela 2 'Tumores (B19-B20)' is a condition, 'Masculino' is a stratum; rodriguez1984 Tabela 2 '1:4' is a condition, '7' (months of age) is a stratum.",
	"8 STRATUM FIELDS ONCE, WITH PAGE. Fill each stratum field from wherever the document prints it (methods, caption, footnote, abstract, figure note) and put the page in field_pages. A field printed once for the whole study goes on s1 and the others inherit it; a stratum repeats it only when its own value differs. null only when printed nowhere. When the stratum label comes from a table stub or header, its page is the table's and needs no field_pages entry. Never take a place from the authors' affiliation or the journal's city: 'Rev. Saúde públ., S. Paulo' is the journal, not the study place. case_definition_as_printed quotes what counted as a case or a positive ('títulos de anticorpos maior ou igual a 1:1', 'adequação inferior a 80%'), diagnostic_method_as_printed the test ('imunofluorescência indireta', 'método de Kato-Katz', 'prova tuberculínica'), data_source_as_printed where the numbers came from ('fichas ... notificados à Secretaria de Saúde do Estado de Pernambuco'), each at most 15 words.",
	"9 TABLE AXES BEFORE RECORDS. For every results, figure_labeled and text entry, fill table_level_labels before any record: what the rows are, what the columns are, the layout, whether it is printed rotated, the period, unit and rate base the caption gives the whole table, every printed total and summary row or column with its label, every heading row, symbol, footnote and 'Fonte:' line. Then fill columns[]: one entry per printed column with its full header and its role.",
	"10 FULL HEADERS. header_as_printed copies the whole header, top line to bottom line, spanning headers joined with ' / ' ('Protegidos / Nº', '1976 / Plasmodium vivax / Masc', 'Nº de pessoas submetidas ao exame de fezes'), units and markers included. Never cut a header. A stub or label broken over two lines by the layout is joined with one space, in printed order (albuquerque1989 Tabela 3: '1960' over '64' gives '1960 64'; Tabela 6: 'Apresentação' over 'espontânea' gives 'Apresentação espontânea').",
	"11 COLUMN ROLES, closed examples. row_label = the stub (Anos, Idade (Meses), Municípios, Grupo de causas, Estado Nutricional); value = a column of numbers ('Masc.', 'Nº', '%', 'Prevalência Inicial', '1ª'); total = a column that adds the others of its row ('Total', 'Total reatores' when it adds weak and strong reactors); code = a printed code column; rank_or_order = a printed order column, not data; statistic_test = a P, χ², t, odds ratio or confidence-limit column, counted and skipped (rule STATISTICS ARE NOT DATA); other.",
	"12 ONE RECORD PER PRINTED DATA CELL. Every body cell that prints a number (0 included), a class or a defined symbol is a data cell and gives one record: counts, rates, percentages, means, medians, totals, subtotals and population figures. Not data cells: headers, stub labels, heading rows without values, rank numbers, blank cells, and '-' or '—' unless the legend defines the dash (then value_kind = symbol, value = null, never converted to 0). A cell that prints two quantities (rodriguez1984 Tabela 5: '20 (11,5)', a count and its percentage) is two data cells: the printed column gets two columns[] entries with the same header_as_printed and cell_part 'first' and 'second'. A number in parentheses that the legend calls a rank (pereira1980 Tabela 2: '102.1 (2)', '** Entre parêntesis = Classificação por ordem de ocorrência') is not a second data cell: it goes to rank_as_printed of the record.",
	"13 HEADING ROWS THAT PRINT VALUES ARE DATA ROWS. A region or group row that prints its own numbers is a data row: its records point to the region stratum, and is_total is true only when the label or the legend says it is a total (a region estimate is not a sum of its states). A heading row that prints no value ('NORDESTE' and 'SUDESTE(*)' in camargo1984 Tabela I, p9; 'Região do Mamanguape' in coura1987 Tabela 1, p3) is a heading_level and the parent stratum of the rows under it.",
	"14 TOTALS ARE RECORDS, NEVER RECOMPUTED. A printed total ('Total', 'Todas as causas', 'Total reatores', 'Sub-total') is recorded like any other cell, with is_total = true and total_kind: row_total = adds across its row (albuquerque1989 Tabela 6: the 1970-85 block next to 1970-77 and 1978-85), column_total = adds down its column, grand_total = the corner cell, subtotal = a partial sum ('Sub-total' in pereira1980 Tabela 3; the '8 a 15' row of rodriguez1984 Tabela 1, which adds part of the rows above); these four are only for cells that add the cells they sit beside. overall = a cell of a printed total row or column that is the rate, mean or share of the whole, not a sum: the 'Total' row of a prevalence, coefficient or mean column, and the cells of a 'Total' column that hold a percentage across the row (ferreira1988 'Total / %'). A summary row not labelled as a total ('Médias' in coura1987 Tabela 1, 'Média', 'Mediana') has is_total = false and its statistic. A '%' total of 100,0 adds the shares: is_total = true, statistic percentage_share, total_kind column_total or row_total. Never fix, recompute or check a total during transcription; the sums are checked by script after adjudication.",
	"15 MEASURE, closed list, one per record. cases = persons with the disease or event counted ('Nº de casos', 'Nº positivo' is positive_results, see below); deaths; population = population counts or estimates and their shares ('População (%)'); persons_examined = people tested or measured, the denominator of a survey ('Nº de crianças', 'Nº de pessoas submetidas ao exame de fezes', 'Nº Total'); tests_done = tests or slides when the document counts tests, not people ('lâminas examinadas'); positive_results = people or tests positive or reactive ('Nº Positivo', 'Reatores fortes / n.º'); negative_results ('Não reatores / n.º'); persons_in_category = people counted in a class that is neither positive nor negative (a nutritional class, a titre class, a detection mode, a parasitaemia class); vaccinated; prevalence = share of examined people with the condition at one time ('Prevalência %', 'Estimativa de prevalência (por 100)'); positivity = share of tests positive; incidence_rate; detection_rate = the leprosy 'coeficiente de detecção', kept apart from incidence; mortality_rate ('Coeficiente de mortalidade'); infant_mortality_rate; case_fatality_rate; proportional_mortality ('Mortalidade proporcional'); coverage = vaccination coverage ('cobertura vacinal'); immune_or_protected = share or count with protective antibodies ('Protegidos'); population_at_risk; hospitalizations; hospital_days; sample_units = municipalities, localities, households or schools counted ('N.º total de localidades'); mean_measurement = a mean or median of a measurement (eggs per gram, weight, induration); time_interval ('Tempo Mediano em Meses'); antibody_titre (geometric mean titre, 'MG'); ratio_between_groups ('Relação Masc./Fem.'); other, with the reason in notes. measure_as_printed copies the words of the caption, column header or stub heading that name the quantity ('prevalência', 'Número de crianças', 'coeficiente de detecção', 'Nº', '%'), at most 15 words, and nothing else: never the condition ('de hanseníase' is condition_as_printed), never a period or block heading ('1ª', 'Avaliações Sucessivas'), never a summary row label ('Médias'), never a class or titre ('1:4'). When the column prints only 'Nº' or '%' and the caption names the quantity, the caption's words win (coura1987 Tabela 1: the caption's 'prevalência', not 'Avaliações Sucessivas'; rodriguez1984 Tabela 2: 'Número de crianças', not '1:4').",
	"16 STATISTIC, closed list, one per record. count = a number of people, events, tests or units; rate_or_proportion = a share of a group having the condition, or a rate over a population, with its base in rate_multiplier (a 'Prevalência %' column next to 'Nº positivo' over 'Nº de pessoas submetidas' is rate_or_proportion, multiplier 100); percentage_share = a percentage of a distribution, each part of a whole split into classes, with or without a printed 100,0 (pereira1980 Tabela 3, albuquerque1989 Tabela 6 '%'; camargo1984, the split by sex, which prints no 100,0); cumulative_percentage; mean; geometric_mean; median; dispersion_measure = a standard deviation, semi-interquartile range or similar printed as its own column (albuquerque1989 Tabela 5 'Amplitude Semi-Interquartílica (Q)'); ratio; total is not a statistic (use is_total). Write the statistic on every record and every value column; never leave it to a default (the fisheries pilot lost 422 adjudication lines to a null default).",
	"17 EVERY RECORD CARRIES ITS EFFECTIVE VALUES. measure_standardized, statistic, unit_as_printed, rate_multiplier, rate_denominator_as_printed, data_source_kind and is_estimate are written on every record with the value that applies to that cell, copied from the cell, row, column, caption, footnote or methods; nothing on a record means 'as the column'. The column and the table say where it was read.",
	"18 UNIT AND RATE BASE AS PRINTED. unit_as_printed copies the unit printed for the cell, its column or its table ('%', 'por 100.000 habitantes', 'por mil habitantes', 'por cem mil habitantes', 'ovos/g de fezes', 'meses', 'mm'). rate_multiplier_as_printed copies the base words ('100.000', 'cem mil', 'mil', '100', '%'), rate_multiplier holds the same base as a number (100000, 1000, 100; '%' is 100), and rate_denominator_as_printed the population it is over ('habitantes', 'nascidos vivos', 'escolares examinados'), null when not printed. A unit printed only in the caption or in the methods counts as printed; when the caption prints the full unit ('por cem mil habitantes') and the column an abbreviation, the caption's wording goes to unit_as_printed and the column's to the column notes. Words in a caption or a methods sentence count as printed for the unit and for the denominator. Closed examples: coura1987 p2, 'prevalência inicial da infecção entre os escolares', gives rate_denominator_as_printed 'escolares' to every prevalence of Tabela 1; rodriguez1984, caption 'Número e percentual de crianças vacinadas', gives unit_as_printed 'crianças' to every count of the table and '%' to every percentage. A count carries its unit like any other cell: measure_standardized does not replace it. Never convert a rate to another base and never compute a rate from counts.",
	"19 ESTIMATES. is_estimate = true when the caption, header or methods call the numbers estimates ('Estimativa de prevalência', 'população estimada'), with the page in the column notes; false otherwise. An estimate is copied like any other number.",
	"20 CONDITION AS PRINTED. condition_as_printed copies the disease, cause, form or class the cell is about, from its row, column or caption, at most 15 words ('Doenças Infecciosas e parasitárias', 'Forma V', 'Desnutrição Pregressa', 'Reatores fracos', 'falciparum'), with its code in condition_code_as_printed when a code is printed with it ('(B1-B18)', 'B45'); the classification it belongs to ('lista B ... 8ª revisão') goes once to table_level_labels.classification_as_printed. A row that is the whole of something ('Todas as causas', 'Total') keeps its printed label. Never standardize a disease name and never add an ICD code that is not printed.",
	"21 PERIOD AS PRINTED, PER CELL. period_as_printed holds the most specific period printed for the cell, from its row, column header or caption, exactly as printed ('1960', '1960 64', '1970-77', '1976', 'junho a outubro de 1983', '1977/78'); period_context_as_printed holds the broader period the caption, a table note or the methods print, and it is mandatory on every cell of the table whenever such a period is printed and the cell's own period is narrower or missing: coura1987, the 1984 cells take '1984/85' from the methods; ferraroni1979 Tabela 1 takes the caption's period. It is copied without footnote markers ('1976* - 1977*' gives '1976 - 1977') and never from a paragraph about other cells (coura1987: the abstract's 'de 1978 a 1983' is not the period of the 5th evaluation). A text value without a narrower period takes the period of its paragraph or of the study, as printed and with page in notes; 'no mesmo período' and 'neste período' resolve to the printed period they point to. Never build a date, never add a year the cell does not print, never take a year from the publication date.",
	"22 STRATA OF A CELL. stratum_ids lists the strata the cell belongs to, one per dimension, most specific first: the stratum of its row (an age group, a municipality), the stratum of its column (a sex, vaccinated or not) and the stratum the caption gives the whole table when that is a place or group other than the study. s1 is the ancestor of every stratum, so it is never listed next to another one: a cell gives ['s1'] only when it belongs to no other stratum. Three closed examples. (a) Row or column prints the place: camargo1984 TABELA I, one state per row, gives [the state], never s1; ferreira1988 Tabelas 1 and 2, one municipality per column, give [the municipality]. (b) The caption gives a group or place other than the study: certain1972, 'escolas públicas estaduais da Capital de São Paulo' in the caption, is a stratum and enters every cell of that table next to the age and sex strata. (c) The caption only repeats the study (albuquerque1989, 'Recife, 1960 a 1985' when s1 is Recife 1960-85): nothing enters for the caption, and a cell by sex gives [the sex stratum]. The table entry lists in stratum_ids every stratum with a cell in that entry.",
	"23 AGE AND SEX AS PRINTED. age_group_as_printed copies the label without its footnote marker ('0 - 14', '≥ 15', '10 +', '7 a 10', '7º e 8º', '00 - 11') and age_unit says the unit the document prints for it (years, months, days; not_printed when the document never says). A marker on the label ('02** - 04' in ferraroni1979 Tabela 6, '** Anos') goes to label_footnote_marker, and its meaning, when it gives the unit, is the page for age_unit. sex_as_printed copies the label ('Masc.', 'Fem.', 'M', 'F', 'ambos os sexos'), sex_standardized reads it (male, female, both). An age that is not the age when the data were collected is not an age_group: rodriguez1984 p6 'Idade da Vacinação (Meses)', the age at vaccination, gives strata with stratum_dimension = other, the printed label in stratum_label_as_printed, the header in notes, and age_group_as_printed null. Never derive an age group or sex the table does not print.",
	"24 DATA SOURCE OF EVERY NUMBER. data_source_kind says where the document says the numbers came from: own_survey = the authors' survey, exams or measurements; notification_records = notifications or case files of a health service ('fichas ... notificados à Secretaria de Saúde'); vital_records = death or birth certificates; programme_records = control programme records (SUCAM, PECE); facility_records = hospital or laboratory records (SAME do Hospital de Moléstias Tropicais); population_estimate = a population figure from a statistics office (CODEPLAN, IBGE); cited_publication = another study's numbers reprinted for comparison ('Fonte: Albuquerque (1984) excetuando Rondônia'), with cited_source_as_printed; mixed; not_stated. It is set on the stratum, on the table and on every record (rule EVERY RECORD CARRIES ITS EFFECTIVE VALUES). Cited numbers are kept as records, with a data_source stratum of their own, so they can be left out of the published dataset.",
	"25 COPY NUMBERS EXACTLY. value_as_printed is the cell exactly as printed, without footnote markers, rank in parentheses and dispersion term; value is the number. The only allowed changes are decimal comma to point and dropping a thousands point ('1.274' -> 1274, '2,04' -> 2.04, '102.1' -> 102.1 where the table uses the point as decimal). A point that could be decimal or thousands is decided from the column's other cells and its unit, with notes when not obvious; a table that mixes separators keeps each cell as printed. A printed range ('variou de 1 a 17', '12 - 23' as a value) is one record with value_kind = range, value null, value_min and value_max. A number whose separators cannot be read as one number has value_kind = malformed, value = null; never guess. A superscript or footnote marker on a number goes to footnote_marker.",
	"26 NEVER COMPUTE OR INFER. No sums, shares, rates, means, age bounds or population figures that are not printed; no value read off a chart axis or a map; no ICD code, disease name, place or year that is not printed. If the document does not print the number, it does not go in.",
	"27 STATISTICS ARE NOT DATA. P-values ('< 0.001', 'N.S.', 'p<0,01'), χ² and t values and their critical values ('X² = 23,32', 'X² crítico = 13,27', 'T = 3,06'), odds ratios, relative risks, confidence limits printed as their own cells, regression equations and fitted curves are counted as data cells and skipped, with the count in skipped_reason. Descriptive statistics of the data (mean, median, geometric mean, standard deviation, semi-interquartile range) are data. A table made only of tests is kind statistical_tests.",
	"28 DISPERSION. A dispersion term attached to a value ('± 3,06', '(± 1,2)', 'IC 95%: 1,1-2,3' printed in the same cell) goes to dispersion_as_printed of that record, never a separate record; what it is goes once in table_level_labels.dispersion_meaning_as_printed.",
	"29 TEXT VALUES. A per-place, per-group or per-period number printed only in the body text, the abstract or a figure note is a mandatory record of a text entry (rule TEXT BLOCKS) when no table or labelled figure prints it (albuquerque1989 p5: prevalence '2,04/mil habitantes' in December 1985). The quote (at most 15 words) goes to notes. A text value that repeats a table cell is not recorded again, also when it repeats it in another base or wording (pereira1980: '5,9 por 1.000' repeats a TABELA 2 rate). A text value that contradicts a table is not a record: it goes to source_inconsistency of the table record (ferreira1988: the abstract says 6,0% 'desnutrição aguda', Tabela 2 prints 6,0 for 'Desnutrição Pregressa'; ferraroni1979 p3: 520, 204, 711 and 202 against Tabela 1). Also not records: a hypothetical projection ('supondo que 100% das crianças', rodriguez1984) and a number of another study or place cited in the discussion (Alhandra 1979 in coura1987); a cited study's numbers enter only from a table that prints them next to this study's (rule DATA SOURCE OF EVERY NUMBER).",
	"30 CONTRADICTIONS THE DOCUMENT PRINTS. When the document contradicts itself (text against table, Portuguese abstract against English abstract, caption against methods, two tables giving the same cell two values, a footnote that does not match), record the table value and fill source_inconsistency with both versions and pages, on the record, the table or the stratum it is about. Closed example: albuquerque1989 prints the Recife prevalence as '2,04/mil habitantes' in December 1985 in the Portuguese abstract (p1) and '2.04 per 100,000' in December 1984 in the English abstract (p8). A sum we would have computed is not a contradiction (rule TOTALS ARE RECORDS).",
	"31 ILLEGIBLE CELLS STAY IN. A data cell that cannot be read with confidence is a record with value_kind = illegible, value = null, the best reading in value_as_printed and the doubt in notes. It counts as transcribed.",
	"32 FIGURES AND MAPS. A figure gives records only for the values printed on it (a bar labelled '61,7' in certain1972 Fig. 1); those bars are its rows and it is kind figure_labeled with data_cells = the printed values. Curves, bars and maps without printed values are figure_unlabeled with data_cells = 0. Values are never read off an axis or a colour scale.",
	"33 AS-PRINTED FIELDS HOLD ONLY PRINTED WORDS. Every *_as_printed field holds only the printed words of that thing, at most 15 words: the place without the municipality and state that have their own fields, the method without the sentence around it. Spelling is never corrected ('Warterlow' in ferreira1988 p2; 'Esquistossomosse' in the title of costa1980, a candidate not taken). Our own explanations go to notes, never into an as-printed field. Symbol and code meanings are written once in table_level_labels.symbols, not on each record. notes, source_inconsistency and every other free-text field quote at most 15 words of the document.",
	"34 FOOTNOTES AND 'FONTE:' LINES. Every footnote under a table goes to table_level_labels.footnotes, one entry per printed note even when two notes share a line (split at the markers), with what took it. A 'Fonte:' line goes to source_lines and fills data_source_kind and cited_source_as_printed of the records it covers. A marker on a stratum label ('SUDESTE(*)', '(*) Excluindo São Paulo' in camargo1984) goes to the stratum's label_footnote_marker and its meaning to the stratum notes and, when it changes who is covered, to population_group_as_printed or coverage_gaps_as_printed.",
	"35 page is the PDF page number counted from 1 (first page of the file = 1), not the journal page printed on it. table_or_figure is the label as printed ('Tabela 2', 'TABELA I', 'TABELA 1', 'Fig. 2', 'Gráfico 5', 'text').",
	"36 TWO INDEPENDENT TRANSCRIPTIONS. Each document is transcribed twice, by A and B, each without seeing the other. A script diffs A and B record by record (key: table_id, column_block, row_index, column_id, cell_part; text entries pair by the number) and field by field, and an adjudicator decides every difference against the rendered page. A difference repeated in every record of a column (the same two values of the same field) comes as one diff line with the list of records, and is decided once. The adjudicator writes adjudicated/<doc_id>.json, adjudicated/<doc_id>_decisions.csv and adjudicated/<doc_id>_summary.json with pairs (A and B records paired after the adjudication), a_error_rows and b_error_rows (decision lines against that side: B_right or both_wrong against A, A_right or both_wrong against B, of any unit) and a_error_records and b_error_records (distinct records of that side with at least one record-field line against it, every record of a repeated line counted; omitted and extra records are rows, not records). Both counts, always, never one for the other. Before closing, the adjudicator runs method/check_long_copies.py on its own files and rewrites every hit (rule AS-PRINTED FIELDS). Write transcriber = 'A' or 'B'.",
	"37 END-OF-TRANSCRIPTION CHECKLIST. Before closing, fill end_checklist: strata (each stratum field filled, inherited or not_printed), tables (each entry closes), rows (stub lines printed against distinct row_index per block), totals (every printed total row and column recorded with is_total), columns (every value column with its unit, rate base and period, or not_printed), measures (every value column with its measure and statistic), markers (every footnote marker taken off a number or a label), symbols (every symbol with its meaning or 'undefined'), privacy (individual case lists skipped and no personal identifier written), cited data (records from other publications counted per table), text values, and the sums over tables[].",
]

CHANGES = [
	"2.0, change 1: s1 is never listed next to another stratum, and rule STRATA OF A CELL has three closed examples (row or column prints the place; caption gives another group; caption repeats the study). The record schema refuses stratum_ids with s1 and anything else. The pilot lost 512 decision lines to this, on both sides (351 + 62 against A, 99 against B).",
	"2.0, change 2: measure_as_printed is defined (rule MEASURE): the words that name the quantity, never the condition, a period or block heading, a summary label or a class. 391 lines were both_acceptable over 'de hanseníase', 394 against one side.",
	"2.0, change 3: unit and denominator read in a caption or methods sentence count as printed, with the coura1987 and rodriguez1984 examples (rule UNIT AND RATE BASE AS PRINTED). A count still carries its unit. 659 lines in the pilot.",
	"2.0, change 4: period_context_as_printed is mandatory when a caption, table note or methods prints a broader period, copied without markers (rule PERIOD AS PRINTED, PER CELL). 273 lines in the pilot.",
	"2.0, change 5: total_kind overall for a total row or column that is the rate, mean or share of the whole, not a sum (rule TOTALS ARE RECORDS); row_total, column_total, grand_total and subtotal are only for sums. is_total and total_kind now go together (schema). 86 pilot totals were not sums.",
	"2.0, change 6: part of a distribution is percentage_share even without a printed 100,0 (rule STATISTIC).",
	"2.0, change 7: text values that are not records, with this pilot's examples: projection, another study in the discussion, repetition in another base, contradiction (rule TEXT VALUES). 71 lines and 23 extra records in the pilot.",
	"2.0, change 8: a place or group of a cited study hangs from that study's data_source stratum, which carries the cited study's fields (rule STRATA FIRST). 25 lines in the pilot.",
	"2.0, change 9: an age that is not the age at collection (age at vaccination) is stratum_dimension other (rule AGE AND SEX AS PRINTED).",
	"2.0, change 10: compare.py pairs text records by the number across text entries of the same page, gives an exact label match priority over a punctuation-free one ('Masc' and 'Masc.', '20-29' and '20 — 29'), and writes a difference repeated down a column as one line with the list of records.",
	"2.0, change 11: the adjudicator writes adjudicated/<doc_id>_summary.json with pairs and both error counts, rows and records, for each side (rule TWO INDEPENDENT TRANSCRIPTIONS); merge.py stops without it.",
	"2.0, change 12: the 15-word cap is checked by script during adjudication (method/check_long_copies.py), not only in the merge.",
	"2.0, change 13: the round is judged on two numbers, value and label accuracy and per-field accuracy; per-record accuracy is only a cascade alarm. merge.py prints the three.",
	"Everything else as saude-1.0-pilot; its changes_from_previous lists what it carried from the agricultural rounds and the biodiversity and fisheries pilots.",
]

PLACE_OF_DEFINITION = enum("Where a meaning, unit, period or statement was read.", ["header", "stub", "caption", "footnote", "legend", "methods", "text", "abstract", "figure_note", "other_table"], nullable=True)

DATA_SOURCE_KIND = enum("Rule DATA SOURCE OF EVERY NUMBER.", ["own_survey", "notification_records", "vital_records", "programme_records", "facility_records", "population_estimate", "cited_publication", "mixed", "not_stated"])

MEASURE = enum("Rule MEASURE, closed list.", ["cases", "deaths", "population", "persons_examined", "tests_done", "positive_results", "negative_results", "persons_in_category", "vaccinated", "prevalence", "positivity", "incidence_rate", "detection_rate", "mortality_rate", "infant_mortality_rate", "case_fatality_rate", "proportional_mortality", "coverage", "immune_or_protected", "population_at_risk", "hospitalizations", "hospital_days", "sample_units", "mean_measurement", "time_interval", "antibody_titre", "ratio_between_groups", "other"])

STATISTIC = enum("Rule STATISTIC, closed list.", ["count", "rate_or_proportion", "percentage_share", "cumulative_percentage", "mean", "geometric_mean", "median", "dispersion_measure", "ratio", "other"])

symbol = obj({
	"symbol": {
		"description": "The code, letter, mark or abbreviation as printed ('*', '**', '-', 'N.S.', 'MG', 'SM', '+++', 'V').",
		"type": "string",
	},
	"meaning_as_printed": text("Its meaning as printed, at most 15 words; null when the document defines it nowhere."),
	"page": {
		"description": "PDF page where the meaning is printed; null when meaning_as_printed is null.",
		"type": ["integer", "null"],
		"minimum": 1,
	},
	"place": {"$ref": "#/$defs/place_of_definition"},
})

footnote = obj({
	"marker": text("Footnote marker as printed ('*', '**', '(1)', '1'), or null for an unmarked note."),
	"text": {"description": "The note as printed, at most 15 words.", "type": "string"},
	"page": PAGE,
	"used_for": {"description": "Field, columns or strata that took it, or 'nothing'.", "type": "string"},
})

stratum = obj({
	"stratum_id": {
		"description": "'s1' for the whole study, then 's2', 's3' ... in the order the document presents them.",
		"type": "string",
		"pattern": "^s[0-9]+$",
	},
	"parent_stratum_id": {
		"description": "s1 for a level of an axis, a broader stratum of the same dimension (a region for its states), or the data_source stratum of a cited study for that study's places and groups (rule STRATA FIRST); null only for s1.",
		"type": ["string", "null"],
		"pattern": "^s[0-9]+$",
	},
	"stratum_dimension": enum("Rule STRATA FIRST.", ["study", "place", "population_group", "age_group", "sex", "data_source", "other"]),
	"stratum_label_as_printed": text("The label the document uses for this stratum, as printed, without its footnote marker ('Rio Tinto', 'NORDESTE', '0 - 14', 'Masc.', 'Vacinados', 'Ouro Preto D'Oeste', 'Jauru'); null for s1 when it has none."),
	"label_footnote_marker": text("Marker printed on the label ('*', '**'); null if none (rule FOOTNOTES)."),
	"place_as_printed": text("The place of this stratum as printed, at most 15 words ('Recife', 'zona rural de Ouro Preto D'Oeste', 'escolas públicas estaduais da Capital de São Paulo', 'engenho Pau do Óleo', 'Hospital de Moléstias Tropicais de Manaus')."),
	"place_kind": enum("What the place is.", ["country", "region", "state", "municipality", "district_or_neighbourhood", "locality", "school", "workplace", "health_facility", "other"], nullable=True),
	"municipality": text("Municipality as printed, only when named as the place of this stratum."),
	"stateProvince": text("State as printed ('PE', 'Estado do Paraná', 'Amazonas')."),
	"country": text("Country as printed; null when not printed."),
	"period_as_printed": text("Period of the study or of this stratum as printed ('1960 a 1985', 'junho a outubro de 1983', '1977-1978', 'de 1975 a 1980'); never normalized."),
	"population_group_as_printed": text("Who the numbers are about, as printed, at most 15 words ('escolares do primeiro ano primário', 'crianças de 0 a 60 meses', 'trabalhadores de campo', 'não-vacinadas', 'população rural')."),
	"age_group_as_printed": text("Rule AGE AND SEX AS PRINTED."),
	"age_unit": enum("Unit the document prints for the age labels of this stratum.", ["years", "months", "days", "not_printed"], nullable=True),
	"sex_as_printed": text("Rule AGE AND SEX AS PRINTED."),
	"sex_standardized": enum(None, ["male", "female", "both"], nullable=True),
	"data_source_as_printed": text("Where the numbers came from, as printed, at most 15 words."),
	"data_source_kind": {"$ref": "#/$defs/data_source_kind"},
	"cited_source_as_printed": text("For cited_publication: the source as printed ('Albuquerque¹ (1984)', 'ENDEF', 'UFMT'); else null."),
	"collected_by_as_printed": text("Institution that collected the data, as printed ('SUCAM', 'Secretaria de Saúde do Distrito Federal'); never a person's name."),
	"case_definition_as_printed": text("What counted as a case, positive or class, as printed, at most 15 words."),
	"diagnostic_method_as_printed": text("Test, exam or classification used, as printed, at most 15 words."),
	"sample_size_as_printed": text("Size of the group as printed in methods or text ('1.274 crianças', '9.155 indivíduos', '3.923 fichas'), at most 15 words. A size printed in a table cell is a record, not this field."),
	"sampling_as_printed": text("How the group was chosen, as printed, at most 15 words ('amostragem sistemática', 'conglomerados de domicílios')."),
	"coverage_gaps_as_printed": text("Printed exclusions and gaps ('Excluindo São Paulo', 'Os óbitos fetais não foram incluídos'), at most 15 words."),
	"field_pages": {
		"description": "Page of each filled field: {field name: page}. Inherited fields and labels read from a table stub are not repeated.",
		"type": "object",
		"additionalProperties": PAGE,
	},
	"source_inconsistency": text("Contradiction the document prints about this stratum, both versions and pages."),
	"notes": text("Anything else, at most 15 words quoted."),
})

table = obj({
	"table_id": {
		"description": "'k1', 'k2' ... in page order; one per page for a continued table.",
		"type": "string",
		"pattern": "^k[0-9]+$",
	},
	"page": {"description": "PDF page (from 1) of this entry.", "type": "integer", "minimum": 1},
	"label": {
		"description": "Label as printed ('Tabela 2', 'TABELA I', 'Fig. 3', 'Gráfico 5'), 'text', or 'Tabela 1, nota' for a note entry. A continuation keeps the label.",
		"type": "string",
	},
	"kind": enum("results = counts, rates or descriptive statistics, of this study or cited; individual_case_list (rule PRIVACY FIRST); stratum_context = lists of places, schools or groups without values; methods_context = sampling plans, formulas, questionnaires; statistical_tests (rule STATISTICS ARE NOT DATA); figure_labeled; figure_unlabeled; text.", ["results", "individual_case_list", "stratum_context", "methods_context", "statistical_tests", "figure_labeled", "figure_unlabeled", "text"]),
	"caption_summary": text("The caption in our own words or quoted, at most 15 words quoted."),
	"printed_rotated": {
		"description": "true when the table or figure is printed turned on the page (certain1972 Tabelas 1 and 2).",
		"type": "boolean",
	},
	"stratum_ids": {
		"description": "Strata with a cell in this entry, on this page. Empty for entries that give no records.",
		"type": "array",
		"items": STRATUM_ID,
	},
	"data_cells": {
		"description": "Data cells, counted before transcription (rule ONE RECORD PER PRINTED DATA CELL), test-statistic cells included. 0 for individual_case_list, stratum_context, methods_context and figure_unlabeled.",
		"type": "integer",
		"minimum": 0,
	},
	"transcribed": {
		"description": "Records written from this entry; must equal the records with this table_id.",
		"type": "integer",
		"minimum": 0,
	},
	"skipped_cells": {"description": "data_cells - transcribed.", "type": "integer", "minimum": 0},
	"skipped_reason": text("Which cells were skipped and why, with counts ('P column, 9 cells'; 'X² line, 3 cells'). Null when skipped_cells = 0."),
	"privacy_skip": {"description": "true for an individual_case_list; false otherwise.", "type": "boolean"},
	"table_level_labels": {
		"description": "Required for results, figure_labeled and text entries; null for the others.",
		"oneOf": [{"$ref": "#/$defs/table_level_labels"}, {"type": "null"}],
	},
	"columns": {
		"description": "One entry per printed column (two for a column whose cells print two quantities) of an entry that gives records; empty otherwise.",
		"type": "array",
		"items": {"$ref": "#/$defs/column"},
	},
	"notes": text("Printed rotated, continues on the next page, text layer unusable, number of rows of an individual case list; at most 15 words quoted."),
})

table_level_labels = obj({
	"row_axis": enum("What the rows are.", ["places", "age_groups", "sex", "population_groups", "periods", "conditions", "classes", "measures", "data_sources", "mixed", "other"]),
	"row_axis_as_printed": text("The stub header as printed ('Anos', 'Idade (Meses)', 'Municípios', 'Grupo de causas *', 'Estado Nutricional'), or null when the stub has none."),
	"column_axis": enum("What the columns are.", ["places", "age_groups", "sex", "population_groups", "periods", "conditions", "classes", "measures", "data_sources", "mixed", "other"]),
	"layout": enum("single_block; side_by_side_blocks = the same columns printed twice or more side by side; stacked_blocks = the same columns printed again below under a new header (ferraroni1979 Tabela 1); transposed; continued = this entry continues a table from the previous page.", ["single_block", "side_by_side_blocks", "stacked_blocks", "transposed", "continued"]),
	"table_period_as_printed": text("Period the caption or a note gives the whole table, as printed ('Recife, 1960 a 1985', 'junho a outubro de 1983', '1977/78')."),
	"table_period_place": {"$ref": "#/$defs/place_of_definition"},
	"unit_statement_as_printed": text("Unit the caption or a note gives the whole table, as printed ('(por 100.000 habitantes)', 'por cem mil habitantes', '(%)'), else null."),
	"rate_base_statement_as_printed": text("The rate base and population the caption or a note gives the whole table, as printed ('por cem mil habitantes'), else null."),
	"quantity_meaning_as_printed": text("What the numbers are, as printed, with page and place when not in the caption ('Coeficiente de mortalidade', 'Estimativa de prevalência')."),
	"case_definition_as_printed": text("Case or class definition the caption or a note gives the table, at most 15 words; else null."),
	"classification_as_printed": text("Classification the table's conditions follow, as printed ('lista B da Classificação Internacional de Doenças, 8ª revisão', 'classificação de Gomez'), else null."),
	"dispersion_meaning_as_printed": text("What a ± or parenthesis term is, as printed; null when no dispersion is printed."),
	"printed_totals": {
		"description": "Every printed total and summary row or column (rule TOTALS ARE RECORDS).",
		"type": "array",
		"items": obj({
			"label_as_printed": {
				"description": "The label exactly as printed ('Total', 'Todas as causas', 'Sub-total', 'Médias', '8 a 15', 'Total reatores').",
				"type": "string",
			},
			"axis": enum(None, ["row", "column", "block"]),
			"kind": enum("Sums: row_total, column_total, grand_total, subtotal, cumulative_total. overall = a total row or column that is the rate, mean or share of the whole, not a sum. mean, median = summary rows not labelled as totals.", ["row_total", "column_total", "grand_total", "subtotal", "cumulative_total", "overall", "mean", "median", "other"]),
			"cells": {"description": "Data cells in that row, column or block.", "type": "integer", "minimum": 0},
		}),
	},
	"heading_levels": {
		"description": "Printed heading rows without values that group the rows, top-down ('Região do Mamanguape', 'Região do Curimataú').",
		"type": "array",
		"items": {"type": "string"},
	},
	"symbols": {
		"description": "Every symbol, code or mark used in the cells, stub or header, once.",
		"type": "array",
		"items": {"$ref": "#/$defs/symbol"},
	},
	"footnotes": {
		"description": "Every footnote and note under the table, one per printed note (rule FOOTNOTES).",
		"type": "array",
		"items": {"$ref": "#/$defs/footnote"},
	},
	"source_lines": {
		"description": "Every 'Fonte:' line as printed, at most 15 words each.",
		"type": "array",
		"items": {"type": "string"},
	},
	"data_source_kind": {"$ref": "#/$defs/data_source_kind"},
	"source_inconsistency": text("Contradiction the document prints about the table as a whole, both versions and pages."),
})

column = obj({
	"column_id": {
		"description": "'c1', 'c2' ... left to right; across blocks the numbering continues. Text entries have one column, c1.",
		"type": "string",
		"pattern": "^c[0-9]+$",
	},
	"column_block": {
		"description": "Block of a side-by-side or stacked layout, from 1; 1 for a single block.",
		"type": "integer",
		"minimum": 1,
	},
	"cell_part": enum("whole for an ordinary column; first and second for the two quantities of a column whose cells print two ('20 (11,5)').", ["whole", "first", "second"]),
	"header_as_printed": {"description": "Rule FULL HEADERS.", "type": "string"},
	"role": enum("Rule COLUMN ROLES.", ["row_label", "value", "total", "code", "rank_or_order", "statistic_test", "other"]),
	"measure_standardized": {
		"description": "For value and total columns: the measure (rule MEASURE). Null for label, code, rank and statistic_test columns, and for a column whose rows carry different measures (then each record says it).",
		"oneOf": [{"$ref": "#/$defs/measure"}, {"type": "null"}],
	},
	"condition_as_printed": text("The condition or class the column holds when the columns are conditions ('Reatores fortes', 'V', 'falciparum', '1:4'), else null."),
	"unit_as_printed": text("Rule UNIT AND RATE BASE AS PRINTED, for this column; null when printed nowhere or not applicable."),
	"unit_source_place": enum("Where the unit was read, or not_printed after header, caption, footnotes, methods and text were searched; not_applicable for label columns.", ["header", "caption", "footnote", "methods", "text", "not_printed", "not_applicable"]),
	"rate_multiplier_as_printed": text("Base words as printed ('100.000', 'cem mil', 'mil', '%'), else null."),
	"rate_multiplier": {"description": "The same base as a number (100000, 1000, 100), else null.", "type": ["number", "null"]},
	"rate_denominator_as_printed": text("Population the rate is over, as printed in the header, caption or methods ('habitantes', 'escolares'), else null."),
	"statistic": {
		"description": "Rule STATISTIC; null only for label, code, rank and statistic_test columns.",
		"oneOf": [{"$ref": "#/$defs/statistic"}, {"type": "null"}],
	},
	"is_estimate": {"description": "Rule ESTIMATES.", "type": "boolean"},
	"is_total_column": {
		"description": "true for a column or block that adds the others of its row (rule TOTALS ARE RECORDS).",
		"type": "boolean",
	},
	"period_as_printed": text("The period this column holds, as printed in its header ('1976', '1970-77', '1ª'), else null."),
	"period_status": enum("filled when the column prints its period, from_row when each row prints it, from_table when only the caption does, not_printed, not_applicable for label columns.", ["filled", "from_row", "from_table", "not_printed", "not_applicable"]),
	"stratum_id": {
		"description": "The stratum this column holds (a sex, a municipality, vaccinated or not), else null.",
		"type": ["string", "null"],
		"pattern": "^s[0-9]+$",
	},
	"notes": text("What a header abbreviation means and the page of its key, where an estimate or unit was read, at most 15 words quoted."),
})

record = obj({
	"record_id": {
		"description": "'r1', 'r2' ... in reading order: table by table, block by block, row by row, left to right.",
		"type": "string",
		"pattern": "^r[0-9]+$",
	},
	"table_id": {"description": "tables[] entry of this record.", "type": "string", "pattern": "^k[0-9]+$"},
	"column_id": {"description": "columns[] entry of this record's cell.", "type": "string", "pattern": "^c[0-9]+$"},
	"cell_part": enum("As the column: whole, first or second.", ["whole", "first", "second"]),
	"page": {"description": "PDF page of the cell; the page of its table entry.", "type": "integer", "minimum": 1},
	"table_or_figure": {"description": "Label as printed, or 'text'.", "type": "string"},
	"column_block": {
		"description": "Block of a side-by-side or stacked layout, from 1; 1 for a single block.",
		"type": "integer",
		"minimum": 1,
	},
	"row_index": {
		"description": "Line of the cell inside its entry and block, from 1, over data lines only (heading rows without values not counted, total and summary rows counted). For a text entry, the order of the number in the block. The key that ties A and B together.",
		"type": "integer",
		"minimum": 1,
	},
	"row_label_as_printed": {
		"description": "The stub cell of this row exactly as printed, without its code and footnote marker ('1960', '0 - 14', 'Doenças Infecciosas e parasitárias', 'Rio Tinto', 'Total'); the quoted words for a text value.",
		"type": "string",
	},
	"row_code_as_printed": text("A code printed with the stub label ('(B1-B18)', 'B45'), else null."),
	"stratum_ids": {
		"description": "Rule STRATA OF A CELL: one stratum per dimension, most specific first; ['s1'] only for a cell that belongs to no other stratum, and s1 never next to another stratum.",
		"type": "array",
		"minItems": 1,
		"items": STRATUM_ID,
	},
	"period_as_printed": text("Rule PERIOD AS PRINTED, PER CELL; null only when the document prints no period for the cell."),
	"period_context_as_printed": text("Rule PERIOD AS PRINTED, PER CELL: the broader period a caption, table note or the methods print, without footnote markers; mandatory when printed and period_as_printed is narrower or null; else null."),
	"condition_as_printed": text("Rule CONDITION AS PRINTED; null only when the cell is about no condition (a population count, a sample size)."),
	"condition_code_as_printed": text("Code printed with the condition ('B1-B18'), else null."),
	"measure_standardized": {"$ref": "#/$defs/measure"},
	"measure_as_printed": {
		"description": "Rule MEASURE: the words of the caption, column header or stub heading that name the quantity ('Coeficiente de mortalidade', 'prevalência', 'Número de crianças', 'Nº', '%'), at most 15 words; never the condition, a period or block heading, a summary row label or a class.",
		"type": "string",
	},
	"value_kind": enum("numeric; range (rule COPY NUMBERS EXACTLY); class (a printed class or word); symbol (a defined symbol, value null); malformed; illegible.", ["numeric", "range", "class", "symbol", "malformed", "illegible"]),
	"value": {
		"description": "The number, decimal point, thousands separator dropped. Null for range, class, symbol, malformed and illegible.",
		"type": ["number", "null"],
	},
	"value_min": {
		"description": "For a range: the lower number as printed, as a number; else null.",
		"type": ["number", "null"],
	},
	"value_max": {"description": "For a range: the upper number; else null.", "type": ["number", "null"]},
	"value_as_printed": {
		"description": "The cell exactly as printed, without footnote markers, rank in parentheses and dispersion term ('5,7', '102.1', '1.274', '< 1', '0,0').",
		"type": "string",
	},
	"dispersion_as_printed": text("Dispersion term attached to the value, as printed ('± 3,06'); null if none."),
	"rank_as_printed": text("A rank printed in the cell ('(2)' in pereira1980 Tabela 2), as printed; null if none."),
	"footnote_marker": text("Footnote or superscript marker printed on the value or the row label, as printed ('*', '**', '1'); null if none."),
	"unit_as_printed": text("Rule UNIT AND RATE BASE AS PRINTED: the unit that applies to this cell; null when printed nowhere."),
	"rate_multiplier_as_printed": text(),
	"rate_multiplier": {"type": ["number", "null"]},
	"rate_denominator_as_printed": text(),
	"statistic": {"$ref": "#/$defs/statistic"},
	"is_estimate": {"description": "Rule ESTIMATES.", "type": "boolean"},
	"is_total": {
		"description": "Rule TOTALS ARE RECORDS: true for a cell in a printed total row, column or block.",
		"type": "boolean",
	},
	"total_kind": enum("Rule TOTALS ARE RECORDS. Required when is_total = true, null otherwise. overall = a total that is the rate, mean or share of the whole, not a sum; the other kinds are sums.", ["row_total", "column_total", "grand_total", "subtotal", "cumulative_total", "overall"], nullable=True),
	"data_source_kind": {"$ref": "#/$defs/data_source_kind"},
	"cited_source_as_printed": text("For cited_publication: the source as printed; else null."),
	"source_inconsistency": text("Contradiction the document prints about this cell, both versions and pages."),
	"notes": text("Reading doubts, the decision on an ambiguous point, the quote for a text value (at most 15 words)."),
}, "One printed data cell of a results table, labelled figure or text block.")
record["allOf"] = [
	# Change 1: s1 is the ancestor of every stratum, so it is listed only alone
	{"if": {"properties": {"stratum_ids": {"contains": {"const": "s1"}}}}, "then": {"properties": {"stratum_ids": {"maxItems": 1}}}},
	# Change 5: a total says its kind, and only a total has one
	{"if": {"properties": {"is_total": {"const": True}}}, "then": {"properties": {"total_kind": {"type": "string"}}}, "else": {"properties": {"total_kind": {"type": "null"}}}},
]

end_checklist = obj({
	"strata": {
		"description": "One entry per stratum and field.",
		"type": "array",
		"items": obj({
			"stratum_id": STRATUM_ID,
			"field": enum(None, ["place_as_printed", "municipality", "stateProvince", "period_as_printed", "population_group_as_printed", "age_group_as_printed", "age_unit", "sex_as_printed", "data_source_as_printed", "collected_by_as_printed", "case_definition_as_printed", "diagnostic_method_as_printed", "sample_size_as_printed", "sampling_as_printed", "coverage_gaps_as_printed"]),
			"status": enum("filled, inherited (from the parent stratum), not_applicable (an age field on a place stratum), or not_printed after the whole document was read.", ["filled", "inherited", "not_applicable", "not_printed"]),
			"page": {
				"description": "Page where it is printed (of the parent when inherited); null when not_applicable or not_printed.",
				"type": ["integer", "null"],
				"minimum": 1,
			},
		}),
	},
	"tables": {
		"description": "One entry per tables[] entry.",
		"type": "array",
		"items": obj({
			"table_id": TABLE_ID,
			"data_cells": COUNT,
			"transcribed": COUNT,
			"skipped_cells": COUNT,
			"closes": {
				"description": "true only when data_cells = transcribed + skipped_cells and transcribed equals the records with this table_id.",
				"type": "boolean",
			},
		}),
	},
	"rows": {
		"description": "One entry per entry that gives records and per block.",
		"type": "array",
		"items": obj({
			"table_id": TABLE_ID,
			"column_block": PAGE,
			"lines_printed": {
				"description": "Data lines printed in the block (heading rows without values excluded, total and summary lines included).",
				"type": "integer",
				"minimum": 0,
			},
			"distinct_row_index_in_records": COUNT,
			"lines_without_records": {
				"description": "row_index of lines that gave no record, with the reason ('7: every cell a dash').",
				"type": "array",
				"items": {"type": "string"},
			},
			"rows_match": {
				"description": "true only when lines_printed = distinct_row_index_in_records + lines_without_records.",
				"type": "boolean",
			},
		}),
	},
	"totals": {
		"description": "One entry per entry that gives records.",
		"type": "array",
		"items": obj({
			"table_id": TABLE_ID,
			"printed_total_rows_columns_blocks": {
				"description": "Labels of every printed total row, column and block, as in table_level_labels.printed_totals.",
				"type": "array",
				"items": {"type": "string"},
			},
			"total_cells_printed": COUNT,
			"records_with_is_total": COUNT,
			"all_totals_recorded": {"description": "true only when the two counts are equal.", "type": "boolean"},
		}),
	},
	"columns": {
		"description": "One entry per entry that gives records.",
		"type": "array",
		"items": obj({
			"table_id": TABLE_ID,
			"value_columns": COUNT,
			"with_unit": COUNT,
			"unit_from_caption_methods_or_text": {
				"type": "array",
				"items": COLUMN_ID,
			},
			"unit_not_printed": {
				"type": "array",
				"items": COLUMN_ID,
			},
			"with_rate_base": {"description": "Value columns that hold rates and print their base.", "type": "integer", "minimum": 0},
			"period_not_printed": {
				"type": "array",
				"items": COLUMN_ID,
			},
			"with_measure_and_statistic": {
				"description": "Must equal value_columns, unless a column's rows carry different measures (then its records do).",
				"type": "integer",
				"minimum": 0,
			},
			"methods_searched": {
				"description": "true when the methods and text were read for every column's unit, rate base, period and case definition.",
				"type": "boolean",
			},
		}),
	},
	"markers": {
		"description": "Every footnote or superscript marker taken off a number or a label.",
		"type": "array",
		"items": obj({
			"table_id": TABLE_ID,
			"marker": {"type": "string"},
			"records": {
				"type": "array",
				"items": RECORD_ID,
			},
			"strata": {
				"description": "Strata whose label carried it.",
				"type": "array",
				"items": STRATUM_ID,
			},
			"meaning_as_printed": text("Its footnote, at most 15 words; null when the document prints none."),
		}),
	},
	"symbols": {
		"description": "Every distinct symbol or code in the document, with its meaning or 'undefined'.",
		"type": "array",
		"items": obj({
			"symbol": {"type": "string"},
			"table_ids": {
				"type": "array",
				"items": TABLE_ID,
			},
			"meaning_as_printed": {"type": "string"},
		}),
	},
	"privacy": obj({
		"individual_case_lists": {
			"description": "table_ids of the entries skipped by rule PRIVACY FIRST.",
			"type": "array",
			"items": TABLE_ID,
		},
		"personal_identifiers_written": {
			"description": "Fields anywhere in the output holding a person's name, address or date of birth. Must be 0.",
			"type": "integer",
			"minimum": 0,
			"maximum": 0,
		},
	}),
	"cited_data": {
		"description": "One entry per entry with records from other publications.",
		"type": "array",
		"items": obj({
			"table_id": TABLE_ID,
			"cited_sources_as_printed": {
				"type": "array",
				"items": {"type": "string"},
			},
			"records_cited": COUNT,
		}),
	},
	"text_values": obj({
		"text_entries": COUNT,
		"text_records": COUNT,
		"text_values_repeating_tables": {
			"description": "Numbers seen in the text that repeat a table cell and were not recorded.",
			"type": "integer",
			"minimum": 0,
		},
		"text_values_contradicting_tables": {
			"description": "Numbers seen in the text that contradict a table and went to source_inconsistency.",
			"type": "integer",
			"minimum": 0,
		},
	}),
	"sums": obj({
		"tables": COUNT,
		"data_cells": COUNT,
		"transcribed": {"description": "Must equal records.", "type": "integer", "minimum": 0},
		"skipped_cells": COUNT,
		"records": COUNT,
		"strata": COUNT,
		"every_table_closes": {"type": "boolean"},
	}),
})

PROPERTIES = {
	"doc_id": enum("Document id from sources.json (also the PDF file name without .pdf).", DOC_IDS) if DOC_IDS else {"description": "Document id from sources.json (also the PDF file name without .pdf).", "type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$"},
	"transcriber": enum("Rule TWO INDEPENDENT TRANSCRIPTIONS.", ["A", "B", "adjudicated"]),
	"schema_version": {"description": "Version of this schema used.", "const": SCHEMA_VERSION, "type": "string"},
	"document_kind": enum("As sources.json documents[].document_kind: survey, surveillance_series, vital_statistics, programme_records, facility_records, mixed.", ["survey", "surveillance_series", "vital_statistics", "programme_records", "facility_records", "mixed"]),
	"strata": {
		"description": "One entry per stratum, s1 first (rules STRATA FIRST, STRATUM FIELDS ONCE).",
		"type": "array",
		"minItems": 1,
		"items": {"$ref": "#/$defs/stratum"},
	},
	"tables": {
		"description": "Rule INVENTORY FIRST, EVERY TABLE AND FIGURE, in page order.",
		"type": "array",
		"items": {"$ref": "#/$defs/table"},
	},
	"records": {
		"type": "array",
		"items": {"$ref": "#/$defs/record"},
	},
	"end_checklist": {"$ref": "#/$defs/end_checklist"},
}

schema = {
	"$schema": "https://json-schema.org/draft/2020-12/schema",
	"$id": "saude/schema.json",
	"title": "Brazilian public health counts and rates in Portuguese-language technical literature, one record per printed data cell",
	"version": SCHEMA_VERSION,
	"description": DESCRIPTION,
	"rules": RULES,
	"type": "object",
	"additionalProperties": False,
	"required": list(PROPERTIES),
	"properties": PROPERTIES,
	"$defs": {
		"place_of_definition": PLACE_OF_DEFINITION, "data_source_kind": DATA_SOURCE_KIND, "measure": MEASURE, "statistic": STATISTIC,
		"symbol": symbol, "footnote": footnote, "stratum": stratum, "table": table, "table_level_labels": table_level_labels,
		"column": column, "record": record, "end_checklist": end_checklist,
	},
	"changes_from_previous": CHANGES,
}

(ROOT / "schema.json").write_text(json.dumps(schema, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("schema.json written:", len(RULES), "rules,", len(DOC_IDS), "doc ids")
