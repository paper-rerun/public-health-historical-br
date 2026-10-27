# Merge the adjudicated documents into records.csv, strata.csv and qa/decisions.csv, check the printed totals against their
# parts (qa/totals_check.csv) and every rate printed next to its numerator and denominator (qa/rates_check.csv), and
# print the pilot numbers for RODADA.md. Both checks are QA only: they never change the data
# Usage: python -X utf8 method/merge.py   (paths are relative to the saude-piloto folder)
#
# Adapted from pesca-piloto/method/merge.py for the public health pilot (schema saude-1.0-pilot). Changed: one kind of
# record and no trials or species key. Records are written as adjudicated, with no inheritance, because rule 17 makes every
# record carry its effective values; the column and table only add fields the record has no place for. Strata still
# inherit from the nearest ancestor that prints a field (rule 8). One-sided rows that the adjudicators paired again
# (pairing artifacts, X, R and S rows, 'paired by number') are not omissions. Records both sides wrote and the
# adjudicator dropped (ferraroni1979 F001) count as extra records on both sides. The self-checks, the long-copy check and
# the printed-totals check are kept; the rate check and the privacy scan are new
import ast
import csv
import glob
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "method"))
import compare  # noqa: E402  only for the compared field lists
MAX_QUOTE_WORDS = 15

# Licence situation per document, read from sources.json (licence)
SCIELO_BY_NC = "CC BY-NC 4.0 (página do artigo no SciELO, lida em 26/10/2026); o PDF não imprime licença"
LICENSE = {
	"camargo1984-chagas-inquerito-nacional-1975-1980": "CC BY 4.0 da revista inteira (página 'about' da Rev. Inst. Med. trop. São Paulo); sem licença do item; o PDF não imprime licença",
	"albuquerque1989-hanseniase-recife-1960-1985": SCIELO_BY_NC,
	"ferreira1988-estado-nutricional-rondonia": SCIELO_BY_NC,
	"rodriguez1984-sarampo-sorologia-curitiba-1983": SCIELO_BY_NC,
	"certain1972-infeccao-tuberculosa-escolares-sp-1970": "não confirmada: a página do SciELO respondeu 502; os outros artigos da Rev. Saúde Pública têm CC BY-NC 4.0",
	"pereira1980-mortalidade-brasilia-1977-1978": SCIELO_BY_NC,
	"ferraroni1979-malaria-amazonas-1972-1977": "CC BY 4.0 (página do artigo no SciELO, lida em 26/10/2026); o PDF não imprime licença",
	"coura1987-pece-esquistossomose-paraiba": SCIELO_BY_NC,
}

# Pairs and one-sided records per document in the adjudication summaries (A records - A only = B records - B only = pairs)
EXPECTED = {
	"camargo1984-chagas-inquerito-nacional-1975-1980": (99, 0, 3, 99),
	"albuquerque1989-hanseniase-recife-1960-1985": (421, 0, 0, 421),
	"ferreira1988-estado-nutricional-rondonia": (168, 0, 0, 168),
	"rodriguez1984-sarampo-sorologia-curitiba-1983": (314, 3, 1, 315),
	"certain1972-infeccao-tuberculosa-escolares-sp-1970": (415, 1, 0, 416),
	"pereira1980-mortalidade-brasilia-1977-1978": (110, 0, 4, 112),
	"ferraroni1979-malaria-amazonas-1972-1977": (657, 0, 0, 653),
	"coura1987-pece-esquistossomose-paraiba": (435, 7, 0, 435),
}
# Kinds of decision row that pair again what compare.py left one-sided
REPAIR_KINDS = {"cross_entry_pair", "paired_by_number", "manual_stratum_pair"}
REPAIR_ID_PREFIXES = ("X", "R", "S")

# Stratum fields a child takes from its parent when it prints nothing of its own (rule 8). The label, dimension, place,
# pages, sample size, inconsistency and notes belong to the stratum that prints them: the survey's '1.626.745 amostras'
# is not the sample of each state
INHERITED_STRATUM_FIELDS = ["municipality", "stateProvince", "country", "period_as_printed", "population_group_as_printed",
	"age_group_as_printed", "age_unit", "sex_as_printed", "sex_standardized", "data_source_as_printed", "data_source_kind",
	"cited_source_as_printed", "collected_by_as_printed", "case_definition_as_printed", "diagnostic_method_as_printed",
	"sampling_as_printed", "coverage_gaps_as_printed"]
# A level of one dimension does not take the parent's value of its own dimension
NOT_INHERITED_BY_DIMENSION = {"age_group": {"age_group_as_printed", "age_unit"}, "sex": {"sex_as_printed", "sex_standardized"},
	"population_group": {"population_group_as_printed"}}
# Column and table fields the record has no place for, copied next to it
EXTRA_COLUMN = {"header_as_printed": "column_header_as_printed", "role": "column_role", "unit_source_place": "unit_source_place",
	"period_status": "column_period_status"}
EXTRA_TABLE = {"label": "table_label", "kind": "table_kind", "printed_rotated": "table_printed_rotated"}
EXTRA_LABELS = {"table_period_as_printed": "table_period_as_printed", "unit_statement_as_printed": "table_unit_statement_as_printed",
	"rate_base_statement_as_printed": "table_rate_base_statement_as_printed", "quantity_meaning_as_printed": "table_quantity_meaning_as_printed",
	"case_definition_as_printed": "table_case_definition_as_printed", "classification_as_printed": "table_classification_as_printed",
	"dispersion_meaning_as_printed": "table_dispersion_meaning_as_printed", "source_lines": "table_source_lines",
	"source_inconsistency": "table_source_inconsistency"}
NOT_SOURCE_TEXT = {"citation", "license", "record_id", "source_record_id", "stratumID", "parentStratumID", "doc_id", "source_file",
	"decision_ids", "inherited"}

NUMBER_FIELDS = {"value", "value_as_printed", "value_kind", "value_min", "value_max", "dispersion_as_printed", "rank_as_printed"}
LABEL_FIELDS = {"row_label_as_printed", "condition_as_printed", "condition_code_as_printed", "row_code_as_printed"}
ONE_SIDED_UNITS = {"stratum": "stratum", "table": "table", "column": "column", "record": "record"}
SUM_KINDS = ("row_total", "column_total", "grand_total", "subtotal")
SUMMARY_STATISTICS = {"mean", "median", "geometric_mean", "dispersion_measure", "ratio"}
RATE_STATISTICS = {"rate_or_proportion", "percentage_share"}
DENOMINATOR_MEASURES = {"persons_examined", "population", "tests_done", "population_at_risk"}
# What a rate or share can be taken of; a count of municipalities is never the numerator of a prevalence (camargo1984)
NUMERATOR_MEASURES = {"cases", "deaths", "positive_results", "negative_results", "persons_in_category", "vaccinated",
	"immune_or_protected", "hospitalizations", "hospital_days", "persons_examined", "population"}

# Quotes: 'x', "x", ‘x’, “x”. The single quote must not touch a letter, so "B's" is not a quote
QUOTE_PATTERN = re.compile(r"(?<![\w])'([^']{3,}?)'(?![\w])|\"([^\"]{3,}?)\"|‘([^’]+)’|“([^”]+)”")
# Privacy scan: a full date, a street or house, a birth date. Hits are printed for a person to read, not asserted away
PRIVACY_PATTERN = re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b(rua|avenida|travessa|logradouro|endereço|nascid[oa] em|data de nascimento)\b", re.IGNORECASE)


def NormalizeWord(word):
	return re.sub(r"^[^\w]+|[^\w]+$", "", word.lower())


def LoadPdfWordShingles(pdf_path):
	# Text layer of the whole PDF, with line-break hyphens joined, as a set of 16-word sequences
	pdf_text = subprocess.run(["pdftotext", "-enc", "UTF-8", pdf_path, "-"], capture_output=True).stdout.decode("utf-8", "replace")
	pdf_text = re.sub(r"-\s*\n\s*", "", pdf_text)
	pdf_words = [NormalizeWord(word) for word in pdf_text.split()]
	pdf_words = [word for word in pdf_words if word]
	shingle_size = MAX_QUOTE_WORDS + 1
	return {tuple(pdf_words[index:index + shingle_size]) for index in range(len(pdf_words) - shingle_size + 1)}


def CopiedRuns(text, pdf_shingles):
	# Word runs of the text found in the PDF text layer with more than MAX_QUOTE_WORDS words in a row
	words = text.split()
	normalized = [NormalizeWord(word) for word in words]
	shingle_size = MAX_QUOTE_WORDS + 1
	runs = []
	index = 0
	while index + shingle_size <= len(words):
		if tuple(normalized[index:index + shingle_size]) in pdf_shingles and "" not in normalized[index:index + shingle_size]:
			run_end = index + shingle_size
			while run_end < len(words) and tuple(normalized[run_end - shingle_size + 1:run_end + 1]) in pdf_shingles:
				run_end += 1
			runs.append(" ".join(words[index:run_end]))
			index = run_end
		else:
			index += 1
	return runs


def LongQuotes(text):
	return [quoted for quoted in (next(group for group in match.groups() if group) for match in QUOTE_PATTERN.finditer(text))
		if len(quoted.split()) > MAX_QUOTE_WORDS]


def StringLeaves(value):
	# A cell that holds a dict or list (JSON, or the Python repr the adjudicators wrote in a_value and b_value) is
	# checked string by string: the quotes around each string are syntax, not a quotation of the source
	if isinstance(value, str):
		if value[:1] in "{[":
			for parser in (json.loads, ast.literal_eval):
				try:
					return StringLeaves(parser(value))
				except (ValueError, SyntaxError, TypeError, MemoryError, RecursionError):
					continue
		return [value]
	if isinstance(value, dict):
		return [leaf for each_value in value.values() for leaf in StringLeaves(each_value)]
	if isinstance(value, list):
		return [leaf for each_value in value for leaf in StringLeaves(each_value)]
	return []


def FindLongCopies(text, pdf_shingles):
	if not isinstance(text, str) or not text:
		return []
	return [copy for leaf in StringLeaves(text) for copy in CopiedRuns(leaf, pdf_shingles) + LongQuotes(leaf)]


def BuildCitation(document):
	authors = "; ".join(document["authors"]).rstrip(".")
	title = document["title"].rstrip(".")
	doi = f" doi:{document['doi']}." if document.get("doi") else ""
	return f"{authors}. {title}. {document['citation'].rstrip('.')}.{doi} Disponível em: {document['record_url']}"


def DecisionIds(item):
	ids = item.get("decision_ids")
	if isinstance(ids, list):
		return "; ".join(str(each_id) for each_id in ids)
	return ids or ""


def SideOfError(decision):
	# Which side a decision counts against. ambiguous_print kept one side's reading and does not count against the other
	if decision == "B_right":
		return ("A",)
	if decision == "A_right":
		return ("B",)
	if decision in ("both_wrong", "corrected"):
		return ("A", "B")
	return ()


def CategoryOf(row):
	# stratum, column, label, record or inventory
	field, index = row["field"], row["a_index"] or row["b_index"]
	if row["table_or_figure"] == "strata":
		return "stratum"
	if field.startswith("columns.") or field == "column":
		return "column"
	if field.startswith("table_level_labels."):
		return "label"
	# table_id is also a record field: a record row carries the record index (r12), a table row the table id (k5)
	if field == "record" or index.lower().startswith("r"):
		return "record"
	return "inventory"


def CellText(value):
	if value is None:
		return ""
	if isinstance(value, (list, dict)):
		return json.dumps(value, ensure_ascii=False) if value else ""
	return value


def StratumRows(doc_id, strata, citation, license_text):
	strata_by_id = {stratum["stratum_id"]: stratum for stratum in strata}
	rows = []
	for stratum in strata:
		row = {"stratumID": f"{doc_id}#{stratum['stratum_id']}",
			"parentStratumID": f"{doc_id}#{stratum['parent_stratum_id']}" if stratum["parent_stratum_id"] else ""}
		for field in compare.STRATUM_FIELDS + ["notes"]:
			if field != "parent_stratum_id":
				row[field] = CellText(stratum[field])
		# Null field: walk up to the first ancestor that prints it
		inherited = []
		for field in INHERITED_STRATUM_FIELDS:
			if field in NOT_INHERITED_BY_DIMENSION.get(stratum["stratum_dimension"], set()):
				continue
			ancestor = stratum
			while ancestor[field] is None and ancestor["parent_stratum_id"]:
				ancestor = strata_by_id[ancestor["parent_stratum_id"]]
			if ancestor is not stratum and ancestor[field] is not None:
				row[field] = CellText(ancestor[field])
				inherited.append(f"{field}:{ancestor['stratum_id']}")
		row["inherited"] = "; ".join(inherited)
		row["doc_id"] = doc_id
		row["origin"] = stratum.get("origin") or ""
		row["decision_ids"] = DecisionIds(stratum)
		row["citation"] = citation
		row["license"] = license_text
		rows.append(row)
	return rows


def FootnoteMeaning(record, labels):
	marker = record.get("footnote_marker")
	if not marker:
		return ""
	bare = marker.strip("()")
	for footnote in (labels.get("footnotes") or []) + (labels.get("symbols") or []):
		printed = footnote.get("marker") or footnote.get("symbol") or ""
		if printed.strip("()") == bare:
			return footnote.get("text") or footnote.get("meaning_as_printed") or ""
	return "(sem nota impressa)"


def Decimals(value_as_printed, value):
	# Decimal places as printed: after the comma, or after a point when the number is not whole
	text = (value_as_printed or "").strip().rstrip("%").strip()
	if "," in text:
		return len(re.sub(r"\D", "", text.rsplit(",", 1)[1]))
	if "." in text and value is not None and float(value) != int(float(value)):
		return len(re.sub(r"\D", "", text.rsplit(".", 1)[1]))
	return 0


def HeaderParts(record):
	return [part.strip() for part in (record["_column_header"] or "").split(" / ")]


def ColumnNumber(column_id):
	match = re.fullmatch(r"c(\d+)", column_id or "")
	return int(match.group(1)) if match else None


def RowParts(total, same_row, allow_totals=False):
	# The cells a row total adds, from the narrowest reading of its header to the widest: its own sub-columns
	# ('1975 / P. vivax' over '1975 / P. vivax / Masc'), its siblings ('Protegidos / Total' beside 'Protegidos / 1:1' ...
	# 'Protegidos / 1:128'), the same tail with the same measure under another head ('1970-85 / Nº' over '1970-77 / Nº' and
	# '1978-85 / Nº'; 'Total reatores / n.º' over the weak and strong reactors, not the 'Não reatores'), then the plain cells
	# of the row with the same period, first with its measure, then any count ('Nº Total' over 'Vacinados / Nº' and
	# 'Não-Vacinados / Nº'). Shares and rates in the row never enter a count, because the statistic must match
	header = HeaderParts(total)
	candidates = [record for record in same_row if record is not total and record["statistic"] == total["statistic"]
		and record["cell_part"] == total["cell_part"] and (allow_totals or (not record["is_total"] and record["_column_role"] == "value"))]
	same_measure = lambda record: record["measure_standardized"] == total["measure_standardized"]
	same_period = lambda record: record["period_as_printed"] == total["period_as_printed"]
	readings = [("children", lambda record, parts: parts[:len(header)] == header and len(parts) > len(header)),
		("siblings", lambda record, parts: len(header) > 1 and len(parts) == len(header) and parts[:-1] == header[:-1]),
		("same_tail", lambda record, parts: len(header) > 1 and parts[1:] == header[1:] and parts[0] != header[0] and same_measure(record)),
		("row_same_measure", lambda record, parts: same_period(record) and same_measure(record)),
		("row_counts", lambda record, parts: same_period(record) and total["statistic"] == "count")]
	for reading, matches in readings:
		parts = [record for record in candidates if matches(record, HeaderParts(record))]
		if parts:
			return reading, parts
	return "", []


def NotASum(total):
	# A total that is not the sum of the cells beside it: a rate or a mean over the whole table (the 'Total' row of a
	# 'Prevalência %' or 'Médias' column), or a share across the row that does not print 100 ('Total / %' of a class is the
	# share of all places, not the sum of each place's share). Rates are checked in qa/rates_check.csv instead
	if total["statistic"] == "rate_or_proportion" or total["statistic"] in SUMMARY_STATISTICS:
		return True
	return total["statistic"] == "percentage_share" and total["total_kind"] == "row_total" and abs(float(total["value"] or 0) - 100) > 1e-9


def PartsOf(total, records):
	# The printed cells a total adds up, by the position the total takes (rule TOTALS ARE RECORDS)
	same_table = [record for record in records if record is not total and record["table_id"] == total["table_id"] and record["page"] == total["page"]]
	kind = total["total_kind"]
	row_above = [record for record in same_table if record["row_index"] == total["row_index"] - 1]
	if kind == "row_total":
		reading, parts = RowParts(total, [record for record in same_table if record["row_index"] == total["row_index"]])
		if not parts:
			# A total printed under its parts, centred on the columns it adds (ferraroni1979 Tabela 3, 'Total de dias por espécie')
			reading, parts = RowParts(total, row_above, allow_totals=True)
			reading = "row_above_" + reading if parts else ""
		return reading, parts
	# Down a column any measure counts: a 'Total' row of children examined adds the class rows above it (ferreira1988)
	in_column = [record for record in same_table if record["column_id"] == total["column_id"] and record["cell_part"] == total["cell_part"]
		and record["statistic"] == total["statistic"] and record.get("total_kind") not in ("column_total", "grand_total", "subtotal")]
	if kind == "grand_total":
		# Down the corner's column: the row totals when it is a total column, the plain cells otherwise; a corner alone in
		# its column adds the column totals in the row above it (ferraroni1979 Tabela 2, 'Total vivax')
		if in_column:
			return "column", in_column
		reading, parts = RowParts(total, row_above, allow_totals=True)
		return ("row_above_" + reading if parts else ""), parts
	if kind == "subtotal":
		# A subtotal labelled with a range of the row labels adds those rows, wherever it is printed (rodriguez1984 Tabela 1:
		# '8 a 15' under the 'Total' row); otherwise the cells above it, back to the previous column total or subtotal
		label_range = re.fullmatch(r"(\S+)\s+(?:a|-|—)\s+(\S+)", (total["row_label_as_printed"] or "").strip())
		row_of_label = {record["row_label_as_printed"]: record["row_index"] for record in in_column}
		if label_range and label_range.group(1) in row_of_label and label_range.group(2) in row_of_label:
			first_row, last_row = row_of_label[label_range.group(1)], row_of_label[label_range.group(2)]
			return "label_range", [record for record in in_column if first_row <= record["row_index"] <= last_row]
		previous_totals = [record["row_index"] for record in same_table if record["column_id"] == total["column_id"]
			and record.get("total_kind") in ("column_total", "grand_total", "subtotal") and record["row_index"] < total["row_index"]]
		floor = max(previous_totals, default=0)
		return "above", [record for record in in_column if floor < record["row_index"] < total["row_index"]]
	# A column of row totals adds its row totals
	plain = [record for record in in_column if not record["is_total"]]
	return "column", plain or in_column


def SumStatus(total, parts):
	# exact, within_rounding or differs, with the sum, the difference and the rounding tolerance
	parts_sum = sum(float(part["value"]) for part in parts)
	difference = float(total["value"]) - parts_sum
	# Each printed number may be rounded by half a unit of the finest digit the total and its parts print
	finest_decimals = max(Decimals(record["value_as_printed"], record["value"]) for record in [total] + parts)
	tolerance = 0.5 * 10 ** -finest_decimals * (len(parts) + 1)
	if abs(difference) < 1e-6:
		status = "exact"
	elif abs(difference) <= tolerance + 1e-9:
		status = "within_rounding"
	else:
		status = "differs"
	return status, round(parts_sum, 6), round(difference, 6), round(tolerance, 6)


def TotalsCheck(doc_id, records):
	# Every printed sum (is_total, total_kind a sum) against the sum of its transcribed parts. A check, not data
	rows = []
	for total in records:
		if not total["is_total"] or total["total_kind"] not in SUM_KINDS:
			continue
		row = {"doc_id": doc_id, "record_id": total["_record_id"], "table_id": total["table_id"], "table_or_figure": total["table_or_figure"],
			"page": total["page"], "row_label_as_printed": total["row_label_as_printed"] or "", "column_header_as_printed": total["_column_header"],
			"total_kind": total["total_kind"], "measure_standardized": total["measure_standardized"], "statistic": total["statistic"],
			"total_as_printed": total["value_as_printed"], "parts_read_as": "", "n_parts": "", "parts_sum": "", "difference": "", "tolerance": "",
			"status": "", "across_sum": "", "note": "", "part_record_ids": ""}
		reading, parts = PartsOf(total, records)
		row["parts_read_as"] = reading
		row["n_parts"] = len(parts)
		row["part_record_ids"] = " ".join(part["_record_id"].split("#")[1] for part in parts)
		if total["value"] is not None and NotASum(total):
			row["status"] = "not_a_sum"
			row["note"] = "a rate, mean or share over the whole table; not the sum of the cells beside it"
		elif total["table_or_figure"] == "text":
			row["status"] = "not_checkable_text"
			row["note"] = "a text total; its parts are not printed next to it"
		elif total["value"] is None:
			row["status"] = "not_checkable_total_not_numeric"
		elif not parts:
			row["status"] = "not_checkable_figure" if total["_table_kind"] == "figure_labeled" else "not_checkable_no_parts"
		elif any(part["value"] is None for part in parts):
			row["status"] = "not_checkable_part_not_numeric"
			row["note"] = "parts not numeric: " + ", ".join(f"{part['value_as_printed']} ({part['value_kind']})" for part in parts if part["value"] is None)
		else:
			row["status"], row["parts_sum"], row["difference"], row["tolerance"] = SumStatus(total, parts)
			if row["status"] == "differs" and total["_table_kind"] == "figure_labeled":
				# A chart prints a value on some bars only, so its total cannot be added up from them
				row["status"] = "not_checkable_figure"
				row["note"] = "only some bars print a value"
		if total["total_kind"] == "grand_total" and total["value"] is not None:
			# The corner cell also adds the column totals of its row
			across = [record for record in records if record["table_id"] == total["table_id"] and record["page"] == total["page"]
				and record["row_index"] == total["row_index"] and record.get("total_kind") == "column_total"
				and record["measure_standardized"] == total["measure_standardized"] and record["statistic"] == total["statistic"]
				and record["value"] is not None]
			if across:
				row["across_sum"] = round(sum(float(record["value"]) for record in across), 6)
		rows.append(row)
	return rows


def RateNumerator(rate, same_row, same_column):
	# The count a rate or share is taken of: the first part of the same cell ('20 (11,5)'), or the count column printed
	# just before it ('Reatores fracos / n.º' before 'Reatores fracos / %', 'Protegidos / Total' before 'Protegidos / %')
	if rate["cell_part"] == "second":
		return next((record for record in same_column if record["row_index"] == rate["row_index"] and record["cell_part"] == "first"
			and record["statistic"] == "count"), None)
	number = ColumnNumber(rate["column_id"])
	if number is None:
		return None
	return next((record for record in same_row if ColumnNumber(record["column_id"]) == number - 1 and record["statistic"] == "count"
		and record["measure_standardized"] in NUMERATOR_MEASURES and record["value"] is not None), None)


def RateCheck(doc_id, records):
	# Every rate or share printed next to the count it is taken of, against that count over each denominator the table
	# prints: a 'Nº de crianças' or 'Nº Total' count in the same row, the column total of the numerator's column, or the
	# row total of the numerator's group. A check, not data: no rate is recomputed in records.csv
	rows = []
	for rate in records:
		if rate["statistic"] not in RATE_STATISTICS or rate["value"] is None or rate["table_or_figure"] == "text":
			continue
		# A '100,0' total of shares is checked as a sum in qa/totals_check.csv
		if rate["is_total"] and rate["statistic"] == "percentage_share":
			continue
		same_table = [record for record in records if record["table_id"] == rate["table_id"] and record["page"] == rate["page"]]
		same_row = [record for record in same_table if record["row_index"] == rate["row_index"]]
		same_column = [record for record in same_table if record["column_id"] == rate["column_id"]]
		numerator = RateNumerator(rate, same_row, same_column)
		if numerator is None:
			continue
		multiplier = float(rate["rate_multiplier"] or 100)
		denominators = []
		for record in same_row:
			if record is not numerator and record["measure_standardized"] in DENOMINATOR_MEASURES and record["statistic"] == "count" and record["value"] is not None:
				denominators.append(("row_" + record["measure_standardized"], record))
		for record in same_table:
			if (record is not numerator and record["column_id"] == numerator["column_id"] and record["cell_part"] == numerator["cell_part"]
					and record.get("total_kind") in ("column_total", "grand_total") and record["value"] is not None):
				denominators.append(("column_total", record))
		for record in same_row:
			if (record is not numerator and record.get("total_kind") in ("row_total", "grand_total") and record["statistic"] == "count"
					and record["value"] is not None and numerator in RowParts(record, same_row)[1]):
				denominators.append(("row_total", record))
		row = {"doc_id": doc_id, "record_id": rate["_record_id"], "table_or_figure": rate["table_or_figure"], "page": rate["page"],
			"row_label_as_printed": rate["row_label_as_printed"] or "", "column_header_as_printed": rate["_column_header"],
			"measure_standardized": rate["measure_standardized"], "statistic": rate["statistic"], "rate_as_printed": rate["value_as_printed"],
			"rate_multiplier": rate["rate_multiplier"] if rate["rate_multiplier"] is not None else "",
			"numerator_record_id": numerator["_record_id"], "numerator_header": numerator["_column_header"], "numerator_as_printed": numerator["value_as_printed"],
			"denominator_kind": "", "denominator_record_id": "", "denominator_as_printed": "", "recomputed": "", "difference": "", "tolerance": "",
			"status": "", "other_denominators": ""}
		tolerance = 0.5 * 10 ** -Decimals(rate["value_as_printed"], rate["value"])
		results = []
		for denominator_kind, denominator in denominators:
			if float(denominator["value"]) == 0:
				continue
			recomputed = float(numerator["value"]) / float(denominator["value"]) * multiplier
			results.append((abs(recomputed - float(rate["value"])), denominator_kind, denominator, recomputed))
		row["tolerance"] = round(tolerance, 6)
		if not results:
			row["status"] = "not_checkable_no_denominator"
		else:
			results.sort(key=lambda result: result[0])
			difference, denominator_kind, denominator, recomputed = results[0]
			row.update(denominator_kind=denominator_kind, denominator_record_id=denominator["_record_id"], denominator_as_printed=denominator["value_as_printed"],
				recomputed=round(recomputed, 4), difference=round(float(rate["value"]) - recomputed, 4))
			# Some authors cut the digits instead of rounding them (rodriguez1984: 32/39 = 82,05 printed 82,0)
			decimals = Decimals(rate["value_as_printed"], rate["value"])
			truncated = int(recomputed * 10 ** decimals + 1e-9) / 10 ** decimals
			if difference <= tolerance + 1e-9:
				row["status"] = "agrees"
			elif abs(truncated - float(rate["value"])) < 1e-9:
				row["status"] = "agrees_truncated"
			elif difference <= 2 * tolerance + 1e-9:
				row["status"] = "within_one_last_digit"
			else:
				row["status"] = "differs"
			row["other_denominators"] = "; ".join(f"{kind} {each['value_as_printed']} -> {round(value, 3)}" for _, kind, each, value in results[1:])
		rows.append(row)
	return rows


def main():
	schema = json.load(open(os.path.join(ROOT, "schema.json"), encoding="utf-8"))
	defs = schema["$defs"]
	sources = json.load(open(os.path.join(ROOT, "sources.json"), encoding="utf-8"))
	documents_by_id = {document["id"]: document for document in sources["documents"]}
	assert set(documents_by_id) == set(EXPECTED) == set(LICENSE)

	shingles_by_doc = {}
	stratum_rows, record_rows, totals_rows, rate_rows = [], [], [], []
	stats = defaultdict(dict)
	privacy_tables = []
	for adjudicated_path in sorted(glob.glob(os.path.join(ROOT, "adjudicated", "*.json"))):
		doc_id = os.path.basename(adjudicated_path)[:-5]
		document = documents_by_id[doc_id]
		shingles_by_doc[doc_id] = LoadPdfWordShingles(os.path.join(ROOT, document["pdf_path"]))
		adjudicated = json.load(open(adjudicated_path, encoding="utf-8"))
		assert adjudicated["doc_id"] == doc_id and adjudicated["document_kind"] == document["document_kind"], doc_id
		assert adjudicated["schema_version"] == "saude-1.0-pilot", doc_id
		citation, license_text = BuildCitation(document), LICENSE[doc_id]

		strata_by_id = {stratum["stratum_id"]: stratum for stratum in adjudicated["strata"]}
		assert adjudicated["strata"][0]["stratum_dimension"] == "study", doc_id
		for stratum in adjudicated["strata"]:
			assert all(field in stratum for field in defs["stratum"]["required"]), (doc_id, stratum.get("stratum_id"))
			assert stratum["parent_stratum_id"] is None or stratum["parent_stratum_id"] in strata_by_id, (doc_id, stratum["stratum_id"])
		stratum_rows += StratumRows(doc_id, adjudicated["strata"], citation, license_text)

		tables_by_id = {table["table_id"]: table for table in adjudicated["tables"]}
		record_fields = defs["record"]["required"]
		effective_records = []
		for record_number, record in enumerate(adjudicated["records"], start=1):
			# Every schema field is there, and the record points to a table, a column and its strata in this document
			assert all(field in record for field in record_fields), (doc_id, record_number)
			assert record["table_id"] in tables_by_id, (doc_id, record_number, record["table_id"])
			table = tables_by_id[record["table_id"]]
			assert not table["privacy_skip"] and table["kind"] != "individual_case_list", (doc_id, record_number)
			columns_by_id = {column["column_id"]: column for column in table.get("columns") or []}
			assert record["column_id"] in columns_by_id, (doc_id, record_number, record["table_id"], record["column_id"])
			assert record["stratum_ids"] and all(stratum_id in strata_by_id for stratum_id in record["stratum_ids"]), (doc_id, record_number)
			# Rule 17: the effective values are on the record
			assert record["measure_standardized"] and record["statistic"] and record["data_source_kind"], (doc_id, record_number)
			column, labels = columns_by_id[record["column_id"]], table.get("table_level_labels") or {}
			row = {"record_id": f"{doc_id}#{record_number:04d}", "doc_id": doc_id, "source_record_id": record["record_id"]}
			for field in record_fields:
				if field != "record_id":
					row[field] = CellText(record[field])
			row["stratum_ids"] = "; ".join(record["stratum_ids"])
			row["stratum_labels"] = " | ".join(strata_by_id[stratum_id]["stratum_label_as_printed"] or "(estudo)" for stratum_id in record["stratum_ids"])
			row["stratum_dimensions"] = "; ".join(strata_by_id[stratum_id]["stratum_dimension"] for stratum_id in record["stratum_ids"])
			for source_field, output_column in EXTRA_TABLE.items():
				row[output_column] = CellText(table.get(source_field))
			for source_field, output_column in EXTRA_COLUMN.items():
				row[output_column] = CellText(column.get(source_field))
			for source_field, output_column in EXTRA_LABELS.items():
				row[output_column] = CellText(labels.get(source_field))
			row["footnote_meaning"] = FootnoteMeaning(record, labels)
			row["notes"] = CellText(record.get("notes"))
			row["origin"] = record.get("origin") or ""
			row["decision_ids"] = DecisionIds(record)
			row["citation"] = citation
			row["license"] = license_text
			record_rows.append(row)
			effective = dict(record)
			effective.update(_record_id=row["record_id"], _column_role=column["role"], _column_header=column["header_as_printed"], _table_kind=table["kind"])
			effective_records.append(effective)
		totals_rows += TotalsCheck(doc_id, effective_records)
		rate_rows += RateCheck(doc_id, effective_records)
		for table in adjudicated["tables"]:
			# Each inventory entry closes (rule 3)
			assert table["data_cells"] == table["transcribed"] + table["skipped_cells"], (doc_id, table["table_id"])
			assert table["transcribed"] == sum(1 for record in adjudicated["records"] if record["table_id"] == table["table_id"]), (doc_id, table["table_id"])
			if table["privacy_skip"] or table["kind"] == "individual_case_list":
				privacy_tables.append((doc_id, table["table_id"], table["label"], table["page"], table["notes"]))
		stats[doc_id].update(kind=adjudicated["document_kind"], final=len(adjudicated["records"]), strata=len(adjudicated["strata"]),
			tables=len(adjudicated["tables"]),
			record_tables=sum(1 for table in adjudicated["tables"] if table["transcribed"]),
			figures_without_values=sum(1 for table in adjudicated["tables"] if table["kind"] == "figure_unlabeled"),
			columns=sum(len(table.get("columns") or []) for table in adjudicated["tables"]),
			data_cells=sum(table["data_cells"] for table in adjudicated["tables"]),
			skipped_cells=sum(table["skipped_cells"] for table in adjudicated["tables"]))

	def WriteCsv(file_name, rows, columns=None):
		columns = columns or list(rows[0].keys())
		with open(os.path.join(ROOT, file_name), "w", encoding="utf-8", newline="") as output_file:
			writer = csv.DictWriter(output_file, fieldnames=columns)
			writer.writeheader()
			writer.writerows(rows)

	os.makedirs(os.path.join(ROOT, "qa"), exist_ok=True)
	WriteCsv("strata.csv", stratum_rows)
	WriteCsv("records.csv", record_rows)
	WriteCsv(os.path.join("qa", "totals_check.csv"), totals_rows)
	WriteCsv(os.path.join("qa", "rates_check.csv"), rate_rows)

	# Concatenate the decision files as they are
	decision_rows = []
	decision_columns = ["source_file"]
	for decisions_path in sorted(glob.glob(os.path.join(ROOT, "adjudicated", "*_decisions.csv"))):
		for row in csv.DictReader(open(decisions_path, encoding="utf-8-sig", newline="")):
			row = {"source_file": "adjudicated/" + os.path.basename(decisions_path), **row}
			for key in row:
				if key not in decision_columns:
					decision_columns.append(key)
			decision_rows.append(row)
	for row in decision_rows:
		for column in decision_columns:
			row.setdefault(column, "")
	WriteCsv(os.path.join("qa", "decisions.csv"), decision_rows, decision_columns)

	# Source text copied past 15 words, or quoted past 15 words, anywhere in the output files
	long_copies = []
	privacy_hits = []
	for file_name, rows, key_of in (("strata.csv", stratum_rows, lambda row: row["stratumID"]),
			("records.csv", record_rows, lambda row: row["record_id"]),
			("qa/decisions.csv", decision_rows, lambda row: f"{row['source_file']} {row['diff_id']}")):
		for row in rows:
			for column, text in row.items():
				if column in NOT_SOURCE_TEXT:
					continue
				for copy in FindLongCopies(text, shingles_by_doc[row["doc_id"]]):
					long_copies.append((file_name, key_of(row), column, copy))
				if isinstance(text, str) and PRIVACY_PATTERN.search(text):
					privacy_hits.append((file_name, key_of(row), column, PRIVACY_PATTERN.search(text).group(0), text[:100]))
	unique_copies = sorted({(file_name, key.split("#")[0] if file_name.endswith("s.csv") and "#" in key else key, column, copy)
		for file_name, key, column, copy in long_copies})
	print(f"long copies: {len(long_copies)} cells, {len(unique_copies)} distinct")
	for copy in unique_copies:
		print("  COPY", copy)
	print("privacy tables skipped:", privacy_tables)
	print(f"privacy scan hits: {len(privacy_hits)}")
	for hit in privacy_hits:
		print("  PRIVACY", hit)

	# Per side and per category: field errors, omissions, extra entries, numbers and labels misread
	field_errors_by_side = Counter()
	error_types = Counter()
	error_examples = {}
	misread_rows = []
	for doc_id in stats:
		a_document = json.load(open(os.path.join(ROOT, "A", doc_id + ".json"), encoding="utf-8"))
		b_document = json.load(open(os.path.join(ROOT, "B", doc_id + ".json"), encoding="utf-8"))
		doc_stats = stats[doc_id]
		doc_stats.update(a_records=len(a_document["records"]), b_records=len(b_document["records"]),
			a_strata=len(a_document["strata"]), b_strata=len(b_document["strata"]), a_tables=len(a_document["tables"]), b_tables=len(b_document["tables"]))
		doc_rows = [row for row in decision_rows if row["doc_id"] == doc_id]
		# Indices paired again after compare.py (X, R and S rows, 'paired by number')
		repaired = {"A": set(), "B": set()}
		for row in doc_rows:
			if row["kind"] in REPAIR_KINDS or row["diff_id"].startswith(REPAIR_ID_PREFIXES):
				repaired["A"].add(row["a_index"])
				repaired["B"].add(row["b_index"])
		counts = Counter()
		wrong = {(side, category): set() for side in "AB" for category in ("record", "stratum", "label", "inventory", "column")}
		for row in doc_rows:
			counts["decision_" + row["decision"]] += 1
			kind, field = row["kind"], row["field"]
			if kind == "adjudicator_finding":
				# Records both sides wrote and the adjudicator dropped (ferraroni1979 F001 'k6 r80-r83'): extra on both sides
				span = re.search(r"r(\d+)-r(\d+)", row["a_index"])
				dropped = int(span.group(2)) - int(span.group(1)) + 1 if span else 1
				counts["dropped_pairs"] += dropped
				for side in SideOfError(row["decision"]):
					counts[f"{side}_record_spurious"] += dropped
					error_types[(side, row[side.lower() + "_error_type"])] += dropped
					error_examples.setdefault((side, row[side.lower() + "_error_type"]), f"{doc_id[:14]} {row['table_or_figure']} p{row['page']}: {row['evidence'][:120]}")
				continue
			if kind.startswith("only_in") or kind == "missing_in_both":
				present_side = kind[-1] if kind.startswith("only_in") else ""
				if (row["decision"] == "pairing_artifact" or row["evidence"].lower().startswith("pairing artifact")
						or (present_side and row[present_side.lower() + "_index"] in repaired[present_side])):
					counts["artifact_rows"] += 1
					continue
				unit = ONE_SIDED_UNITS.get(field, "record")
				if kind == "missing_in_both":
					for side in ("both", "A", "B"):
						counts[f"{side}_{unit}_omitted"] += 1
					continue
				missing_side = "B" if present_side == "A" else "A"
				if unit == "record" and present_side == "A":
					counts["a_only_records"] += 1
				if unit == "record" and present_side == "B":
					counts["b_only_records"] += 1
				if row["decision"] in (present_side + "_right", "ambiguous_print"):
					counts[f"{missing_side}_{unit}_omitted"] += 1
					error_type = row[missing_side.lower() + "_error_type"] or row[present_side.lower() + "_error_type"] or f"{unit}_omitted"
					error_types[(missing_side, error_type)] += 1
					error_examples.setdefault((missing_side, error_type), f"{doc_id[:14]} {row['table_or_figure']} {field}: {row['evidence'][:120]}")
				elif row["decision"] == missing_side + "_right":
					counts[f"{present_side}_{unit}_spurious"] += 1
					error_type = row[present_side.lower() + "_error_type"] or f"{unit}_spurious"
					error_types[(present_side, error_type)] += 1
					error_examples.setdefault((present_side, error_type), f"{doc_id[:14]} {row['table_or_figure']} {field}: {row['evidence'][:120]}")
				else:
					counts[f"{present_side}_{unit}_optional"] += 1
				continue
			category = CategoryOf(row)
			for side in SideOfError(row["decision"]):
				counts[f"{side}_{category}_field_errors"] += 1
				wrong[(side, category)].add(row[side.lower() + "_index"] or row["a_index"] or row["b_index"])
				field_errors_by_side[(side, category, re.sub(r"^(columns\.[^.]+|table_level_labels)\.", "", field))] += 1
				error_type = row[side.lower() + "_error_type"] or "(sem tipo)"
				error_types[(side, error_type)] += 1
				error_examples.setdefault((side, error_type), f"{doc_id[:14]} {row['table_or_figure']} {field}: {row['evidence'][:120]}")
				if category == "record" and field in NUMBER_FIELDS:
					counts[f"{side}_number_errors"] += 1
					misread_rows.append(("number", side, row))
				if category == "record" and field in LABEL_FIELDS:
					counts[f"{side}_label_text_errors"] += 1
		doc_stats.update(counts)
		for (side, category), units in wrong.items():
			doc_stats[f"{side}_wrong_{category}"] = len(units)
		for side in "AB":
			# A table with a label, inventory or column error counts once
			doc_stats[f"{side}_wrong_table"] = len(wrong[(side, "label")] | wrong[(side, "inventory")] | wrong[(side, "column")])
		pairs, a_only, b_only, final = EXPECTED[doc_id]
		doc_stats["pairs"] = doc_stats["a_records"] - counts["a_only_records"]
		assert doc_stats["pairs"] == pairs == doc_stats["b_records"] - counts["b_only_records"], (doc_id, doc_stats["pairs"], counts["a_only_records"], counts["b_only_records"])
		assert (counts["a_only_records"], counts["b_only_records"]) == (a_only, b_only), (doc_id, counts["a_only_records"], counts["b_only_records"])
		# Every final record is a pair kept, or a record one side omitted
		doc_stats["required"] = pairs - counts["dropped_pairs"] + counts["A_record_omitted"] + counts["B_record_omitted"] - counts["both_record_omitted"]
		assert doc_stats["required"] == final == doc_stats["final"], (doc_id, doc_stats["required"], final, doc_stats["final"])

	totals = Counter()
	print("doc_id;kind;final;pairs;strata;tables;A_rec;B_rec;A_wrong_rec;B_wrong_rec;A_omit;B_omit;A_extra;B_extra;"
		"A_wrong_stratum;B_wrong_stratum;A_strat_omit;B_strat_omit;A_strat_extra;B_strat_extra;A_wrong_table;B_wrong_table;A_tab_omit;B_tab_omit;"
		"A_lines;B_lines;A_numbers;B_numbers;both_acceptable;artifacts")
	for doc_id, doc_stats in sorted(stats.items()):
		for key, value in doc_stats.items():
			if isinstance(value, int):
				totals[key] += value
		a_lines = doc_stats.get("decision_B_right", 0) + doc_stats.get("decision_both_wrong", 0) + doc_stats.get("decision_corrected", 0)
		b_lines = doc_stats.get("decision_A_right", 0) + doc_stats.get("decision_both_wrong", 0) + doc_stats.get("decision_corrected", 0)
		print(f"{doc_id};{doc_stats['kind']};{doc_stats['final']};{doc_stats['pairs']};{doc_stats['strata']};{doc_stats['tables']};"
			f"{doc_stats['a_records']};{doc_stats['b_records']};{doc_stats['A_wrong_record']};{doc_stats['B_wrong_record']};"
			f"{doc_stats.get('A_record_omitted', 0)};{doc_stats.get('B_record_omitted', 0)};{doc_stats.get('A_record_spurious', 0)};{doc_stats.get('B_record_spurious', 0)};"
			f"{doc_stats['A_wrong_stratum']};{doc_stats['B_wrong_stratum']};{doc_stats.get('A_stratum_omitted', 0)};{doc_stats.get('B_stratum_omitted', 0)};"
			f"{doc_stats.get('A_stratum_spurious', 0)};{doc_stats.get('B_stratum_spurious', 0)};{doc_stats['A_wrong_table']};{doc_stats['B_wrong_table']};"
			f"{doc_stats.get('A_table_omitted', 0)};{doc_stats.get('B_table_omitted', 0)};{a_lines};{b_lines};"
			f"{doc_stats.get('A_number_errors', 0)};{doc_stats.get('B_number_errors', 0)};{doc_stats.get('decision_both_acceptable', 0)};{doc_stats.get('artifact_rows', 0)}")
	print(dict(sorted(totals.items())))

	# Accuracy per record, stratum and table, counting omissions, with and without the largest document
	largest_doc = max(stats, key=lambda doc_id: stats[doc_id]["required"])
	compared_fields = sum(stats[doc_id]["pairs"] for doc_id in stats) * len(compare.RECORD_FIELDS)
	for side in ("A", "B"):
		required = totals["required"]
		omitted = totals[side + "_record_omitted"]
		wrong_records = totals[side + "_wrong_record"]
		print(f"{side} records: right {required - omitted - wrong_records}/{required} = {100 * (required - omitted - wrong_records) / required:.1f}%"
			f" | omitted {omitted} | with error {wrong_records} | extra {totals[side + '_record_spurious']}")
		record_field_errors = totals[side + "_record_field_errors"]
		print(f"{side} record fields {record_field_errors}/{compared_fields} = {100 * record_field_errors / compared_fields:.2f}%"
			f" | number fields {totals[side + '_number_errors']} | label fields {totals[side + '_label_text_errors']}")
		largest = stats[largest_doc]
		required_rest = required - largest["required"]
		right_rest = required_rest - (omitted - largest.get(side + "_record_omitted", 0)) - (wrong_records - largest[side + "_wrong_record"])
		print(f"{side} records without {largest_doc}: {right_rest}/{required_rest} = {100 * right_rest / required_rest:.1f}%")
		unit_total = totals["strata"]
		unit_omitted = totals[f"{side}_stratum_omitted"]
		wrong_units = totals[f"{side}_wrong_stratum"]
		print(f"{side} strata: right {unit_total - unit_omitted - wrong_units}/{unit_total} = {100 * (unit_total - unit_omitted - wrong_units) / unit_total:.1f}%"
			f" | omitted {unit_omitted} | extra {totals[side + '_stratum_spurious']} | with error {wrong_units} | fields {totals[side + '_stratum_field_errors']}")
		table_total = totals["tables"]
		table_omitted = totals[side + "_table_omitted"]
		wrong_tables = totals[side + "_wrong_table"]
		print(f"{side} tables: right {table_total - table_omitted - wrong_tables}/{table_total} = {100 * (table_total - table_omitted - wrong_tables) / table_total:.1f}%"
			f" | omitted {table_omitted} | extra {totals[side + '_table_spurious']} | with error {wrong_tables}"
			f" | label fields {totals[side + '_label_field_errors']} | inventory fields {totals[side + '_inventory_field_errors']}"
			f" | column fields {totals[side + '_column_field_errors']} | columns omitted {totals[side + '_column_omitted']}")
		for doc_id in sorted(stats):
			doc_stats = stats[doc_id]
			right = doc_stats["required"] - doc_stats.get(side + "_record_omitted", 0) - doc_stats[side + "_wrong_record"]
			print(f"   {side} {doc_id[:22]}: {right}/{doc_stats['required']} = {100 * right / doc_stats['required']:.1f}%")
	print("field errors by side:", sorted(field_errors_by_side.items(), key=lambda item: -item[1])[:40])
	print("error types by side:", sorted(error_types.items(), key=lambda item: -item[1]))
	for key, example in sorted(error_examples.items()):
		print("  EXAMPLE", key, example)
	for what, side, row in misread_rows:
		print("  MISREAD", what, side, row["doc_id"][:14], row["diff_id"], row["table_or_figure"], row["field"], repr(row["a_value"])[:40], repr(row["b_value"])[:40],
			row["decision"], row[side.lower() + "_error_type"], "|", row["evidence"][:140])
	print("decision rows:", len(decision_rows), Counter(row["decision"] for row in decision_rows))
	print("decision rows by category:", sorted(Counter((CategoryOf(row), row["decision"]) for row in decision_rows).items()))
	print("both_acceptable fields:", Counter(row["field"] for row in decision_rows if row["decision"] == "both_acceptable").most_common(12))
	print("artifact rows:", totals["artifact_rows"], "dropped pairs:", totals["dropped_pairs"])
	print("data cells:", totals["data_cells"], "skipped cells:", totals["skipped_cells"], "record tables:", totals["record_tables"],
		"figures without values:", totals["figures_without_values"], "columns:", totals["columns"])

	# What the data hold
	print("records origin:", Counter(row["origin"] for row in record_rows))
	for field in ("measure_standardized", "statistic", "value_kind", "data_source_kind", "table_kind", "rate_multiplier", "unit_as_printed", "total_kind", "is_estimate"):
		print(f"records {field}:", Counter(row[field] for row in record_rows).most_common(25))
	print("records from text:", sum(1 for row in record_rows if row["table_or_figure"] == "text"),
		"source_inconsistency (record):", sum(1 for row in record_rows if row["source_inconsistency"]),
		"(record or table):", sum(1 for row in record_rows if row["source_inconsistency"] or row["table_source_inconsistency"]),
		"with condition code:", sum(1 for row in record_rows if row["condition_code_as_printed"]),
		"rank:", sum(1 for row in record_rows if row["rank_as_printed"]), "dispersion:", sum(1 for row in record_rows if row["dispersion_as_printed"]),
		"period:", sum(1 for row in record_rows if row["period_as_printed"]), "period context:", sum(1 for row in record_rows if row["period_context_as_printed"]),
		"rate denominator:", sum(1 for row in record_rows if row["rate_denominator_as_printed"]))
	print("records by doc and measure:", sorted(Counter((row["doc_id"][:12], row["measure_standardized"]) for row in record_rows).items()))
	print("strata dimension:", Counter(row["stratum_dimension"] for row in stratum_rows), "inherited:",
		Counter(entry.split(":")[0] for row in stratum_rows for entry in row["inherited"].split("; ") if entry))
	print("strata by doc and dimension:", sorted(Counter((row["doc_id"][:12], row["stratum_dimension"]) for row in stratum_rows).items()))
	print("strata data_source_kind:", Counter(row["data_source_kind"] for row in stratum_rows), "place_kind:", Counter(row["place_kind"] for row in stratum_rows))
	print("collected_by / cited_source (people check):", sorted({row["collected_by_as_printed"] for row in stratum_rows if row["collected_by_as_printed"]}
		| {row["cited_source_as_printed"] for row in stratum_rows + record_rows if row["cited_source_as_printed"]}))
	status_counts = Counter(row["status"] for row in totals_rows)
	print("totals check:", len(totals_rows), status_counts, Counter(row["parts_read_as"] for row in totals_rows))
	print("totals by doc and status:", sorted(Counter((row["doc_id"][:14], row["total_kind"], row["status"]) for row in totals_rows).items()))
	for row in totals_rows:
		if row["status"] not in ("exact", "within_rounding") or row["across_sum"] not in ("", row["parts_sum"]):
			print("  TOTAL", row["doc_id"][:14], row["table_or_figure"], row["record_id"].split("#")[1], row["row_label_as_printed"][:25], row["column_header_as_printed"][:30],
				row["total_kind"], row["total_as_printed"], row["parts_read_as"], row["parts_sum"], row["difference"], row["tolerance"], row["status"], row["n_parts"],
				"across", row["across_sum"], row["note"])
	rate_status = Counter(row["status"] for row in rate_rows)
	print("rates check:", len(rate_rows), rate_status, Counter(row["denominator_kind"] for row in rate_rows))
	print("rates by doc and status:", sorted(Counter((row["doc_id"][:14], row["table_or_figure"], row["status"]) for row in rate_rows).items()))
	for row in rate_rows:
		if row["status"] not in ("agrees", "agrees_truncated"):
			print("  RATE", row["doc_id"][:14], row["table_or_figure"], row["record_id"].split("#")[1], row["row_label_as_printed"][:25], row["column_header_as_printed"][:30],
				row["rate_as_printed"], row["numerator_as_printed"], row["denominator_kind"], row["denominator_as_printed"], row["recomputed"], row["difference"],
				row["tolerance"], row["status"], "|", row["other_denominators"])
	unchecked_rates = [row for row in record_rows if row["statistic"] in RATE_STATISTICS and row["table_or_figure"] != "text"
		and row["record_id"] not in {rate["record_id"] for rate in rate_rows}]
	print("rates and shares with no count printed before them:", len(unchecked_rates), Counter((row["doc_id"][:12], row["table_or_figure"]) for row in unchecked_rates))

	# Self-check: every adjudicated record once, every record points to its strata, the checks reach every total, no long copy
	assert len(record_rows) == sum(doc_stats["final"] for doc_stats in stats.values())
	assert len({row["record_id"] for row in record_rows}) == len(record_rows)
	stratum_ids = {row["stratumID"] for row in stratum_rows}
	assert len(stratum_ids) == len(stratum_rows)
	assert all(not row["parentStratumID"] or row["parentStratumID"] in stratum_ids for row in stratum_rows)
	assert all(f"{row['doc_id']}#{stratum_id}" in stratum_ids for row in record_rows for stratum_id in row["stratum_ids"].split("; "))
	assert all(row["statistic"] and row["measure_standardized"] for row in record_rows)
	assert len(decision_rows) == sum(sum(1 for _ in csv.DictReader(open(path, encoding="utf-8-sig"))) for path in glob.glob(os.path.join(ROOT, "adjudicated", "*_decisions.csv")))
	# Every printed sum in the records reaches the totals check
	assert len(totals_rows) == sum(1 for row in record_rows if row["is_total"] is True and row["total_kind"] in SUM_KINDS)
	# A 16-word copy is caught, a 15-word copy is not, and a 16-word quote is caught even when it is not in the PDF
	test_words = [f"w{index}" for index in range(30)]
	test_shingles = {tuple(test_words[index:index + MAX_QUOTE_WORDS + 1]) for index in range(len(test_words) - MAX_QUOTE_WORDS)}
	assert CopiedRuns(" ".join(test_words[:16]) + " x", test_shingles) == [" ".join(test_words[:16])]
	assert CopiedRuns(" ".join(test_words[:15]) + " x", test_shingles) == []
	assert LongQuotes("as in '" + " ".join(["z"] * 16) + "' here") and not LongQuotes("B's and '" + " ".join(["z"] * 15) + "'")
	# A dict repr with a long string of our own words is not a quote, but a long quote inside one of its strings still is
	assert not FindLongCopies(repr({"notes": " ".join(["z"] * 16)}), set())
	assert FindLongCopies(repr({"notes": "p3 says '" + " ".join(["z"] * 16) + "'"}), set())
	assert PRIVACY_PATTERN.search("nascido em 12/03/1975") and not PRIVACY_PATTERN.search("1975/1980 e 1977/78")
	# table_id on a record row (r51) is a record error, on a table row (k5) an inventory error; strata rows are strata
	table_id_row = {"field": "table_id", "table_or_figure": "Tabela 2", "kind": "wording", "a_index": "r51", "b_index": "r51"}
	assert CategoryOf(table_id_row) == "record"
	assert CategoryOf({**table_id_row, "a_index": "k5", "b_index": "k5"}) == "inventory"
	assert CategoryOf({**table_id_row, "table_or_figure": "strata", "a_index": "s2", "b_index": "s2"}) == "stratum"
	# A state with no period takes the study's and says so; an age group keeps its own age and never takes the sample size
	empty = {field: None for field in compare.STRATUM_FIELDS + ["notes"]}
	test_strata = [{**empty, "stratum_id": "s1", "parent_stratum_id": None, "stratum_dimension": "study", "period_as_printed": "1975/1980",
			"age_group_as_printed": "0 a 60 meses", "sample_size_as_printed": "1.626.745 amostras"},
		{**empty, "stratum_id": "s2", "parent_stratum_id": "s1", "stratum_dimension": "place"},
		{**empty, "stratum_id": "s3", "parent_stratum_id": "s1", "stratum_dimension": "age_group"}]
	place, age = StratumRows("t", test_strata, "", "")[1:]
	assert place["period_as_printed"] == "1975/1980" and place["age_group_as_printed"] == "0 a 60 meses" and place["sample_size_as_printed"] == ""
	assert age["age_group_as_printed"] == "" and age["period_as_printed"] == "1975/1980"

	# Totals: a row total adds its own group, a column total its column, a subtotal the cells above it, the corner its column
	def TestRecord(row_index, column_id, value, header, total_kind=None, statistic="count", measure="cases", role="value"):
		return {"_record_id": f"t#{row_index}{column_id}", "table_id": "k1", "page": 1, "row_index": row_index, "column_id": column_id,
			"cell_part": "whole", "measure_standardized": measure, "value": value, "value_as_printed": str(value), "value_kind": "numeric",
			"is_total": total_kind is not None, "total_kind": total_kind, "statistic": statistic, "_column_role": role, "_column_header": header,
			"table_or_figure": "Tabela 1", "row_label_as_printed": str(row_index), "rate_multiplier": 100 if statistic != "count" else None,
			"period_as_printed": "1983", "_table_kind": "results"}
	test_records = [TestRecord(1, "c2", 10, "vivax / Masc"), TestRecord(1, "c3", 5, "vivax / Fem."), TestRecord(1, "c4", 15, "vivax / Total", "row_total", role="total"),
		TestRecord(1, "c5", 4, "falciparum / Masc"), TestRecord(1, "c6", 1, "falciparum / Fem."), TestRecord(1, "c7", 9, "falciparum / Total", "row_total", role="total"),
		TestRecord(2, "c2", 20, "vivax / Masc"), TestRecord(2, "c3", 2, "vivax / Fem."), TestRecord(2, "c4", 22, "vivax / Total", "row_total", role="total"),
		TestRecord(3, "c2", 30, "vivax / Masc", "column_total"), TestRecord(3, "c3", 7, "vivax / Fem.", "column_total"),
		TestRecord(3, "c4", 37, "vivax / Total", "grand_total", role="total"), TestRecord(4, "c2", 15, "vivax / Masc", statistic="mean")]
	test_status = {row["record_id"]: row["status"] for row in TotalsCheck("t", test_records)}
	assert test_status == {"t#1c4": "exact", "t#1c7": "differs", "t#2c4": "exact", "t#3c2": "exact", "t#3c3": "exact", "t#3c4": "exact"}, test_status
	# 'Nº Total' adds counts of two measures and skips the share between them; a prevalence total is not a sum; a total
	# printed under its parts adds the row above
	test_records = [TestRecord(1, "c2", 39, "Nº Total", "row_total", measure="persons_examined", role="total"),
		TestRecord(1, "c3", 32, "Vacinados / Nº", measure="vaccinated"), TestRecord(1, "c4", 82.0, "Vacinados / %", statistic="rate_or_proportion", measure="coverage"),
		TestRecord(1, "c5", 7, "Não-Vacinados / Nº", measure="persons_in_category"),
		TestRecord(2, "c4", 79.0, "Vacinados / %", "column_total", statistic="rate_or_proportion", measure="coverage"),
		TestRecord(3, "c2", 276, "1975 / vivax / Masc", measure="hospital_days"), TestRecord(3, "c3", 69, "1975 / vivax / Fem.", measure="hospital_days"),
		TestRecord(4, "c9", 345, "1975 / vivax", "row_total", measure="hospital_days", role="total")]
	test_rows = {row["record_id"]: (row["status"], row["parts_read_as"]) for row in TotalsCheck("t", test_records)}
	assert test_rows == {"t#1c2": ("exact", "row_counts"), "t#2c4": ("not_a_sum", "column"), "t#4c9": ("exact", "row_above_children")}, test_rows
	assert Decimals("1.166,00", 1166.0) == 2 and Decimals("150.560", 150560) == 0 and Decimals("100.0", 100.0) == 0 and Decimals("102.1", 102.1) == 1
	# Rates: '%' after its count agrees over the row's 'Nº de crianças', and a misprinted one does not
	rate_records = [TestRecord(1, "c2", 200, "N.º de crianças", measure="persons_examined"), TestRecord(1, "c3", 37, "Reatores / n.º", measure="positive_results"),
		TestRecord(1, "c4", 18.5, "Reatores / %", statistic="rate_or_proportion", measure="prevalence"),
		TestRecord(2, "c2", 200, "N.º de crianças", measure="persons_examined"), TestRecord(2, "c3", 37, "Reatores / n.º", measure="positive_results"),
		TestRecord(2, "c4", 19.5, "Reatores / %", statistic="rate_or_proportion", measure="prevalence")]
	rate_status = {row["record_id"]: (row["status"], row["denominator_kind"]) for row in RateCheck("t", rate_records)}
	assert rate_status == {"t#1c4": ("agrees", "row_persons_examined"), "t#2c4": ("differs", "row_persons_examined")}, rate_status
	assert not long_copies, f"{len(long_copies)} cells copy more than {MAX_QUOTE_WORDS} words of the source: rewrite them in adjudicated/"


if __name__ == "__main__":
	main()
