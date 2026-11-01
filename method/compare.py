# Compare the two blind transcriptions of a public health round (A/*.json and B/*.json, schema 2.0, also reads the
# pilot's saude-1.0-pilot files: {strata, tables, records, end_checklist})
# Output: diff_<doc_id>.csv (or diff.csv for every doc in both folders) with strata disagreements first, then table,
# label and column disagreements, then every record field disagreement and every record present on one side only
#
# Schema 2.0 (saude-piloto/RODADA.md, change 10):
# - text records left alone inside their entry pair by the number across every text entry of the same page; table_id and
#   row_index are not compared between two text records, the inventory rows already say how the blocks differ
# - an exact label match scores above a punctuation-free one, for strata and records: 'Masc' pairs with 'Masc' before
#   'Masc.', '20-29' with '20-29' before '20 — 29' (ferraroni1979 lost 78 rows to cross pairs)
# - a record field that differs the same way (same two values) in several records of one column is one line, with
#   cascade_size and the A and B record ids; the adjudicator decides it once (coura1987 '1.ª' was 260 lines)
# - --root and --out; the field lists come from the 2.0 schema next to this script (../schema.json) whatever --root is
#
# Adapted from pesca-piloto/method/compare.py. What changed for this schema:
# - no trials and no species key; one record definition for every cell
# - field lists still come from schema.json ($defs required, minus ids and free text)
# - no inheritance step: rule 17 makes every record carry its effective values, so records are compared as written
# - records pair inside (table, page) by row label, column, cell part, strata, period and condition; text entries
#   (rule 4) pair by the printed number first, not by the line. The value is a tie-breaker elsewhere, so a misread
#   value still pairs
# - the prefix column says when one side's text is the start of the other's (biodiversity lesson 2)
# - end_checklist is not compared, it is recomputed from the final records
#
# Usage: py -3.12 -I -X utf8 compare.py [doc_id ...] [--root DIR] [--out DIR]   (A/ and B/ under --root, default the folder
# above this script; output to --out, default <root>/method); py -3.12 -I -X utf8 compare.py --check runs the asserts only
import csv
import difflib
import glob
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
with open(os.path.join(ROOT, "schema.json"), encoding="utf-8") as schema_handle:
	SCHEMA_DEFS = json.load(schema_handle)["$defs"]


def fields_of(definition, skipped):
	return [field for field in SCHEMA_DEFS[definition]["required"] if field not in skipped]


# Ids are the pairing keys; notes, caption_summary and skipped_reason are free text
STRATUM_FIELDS = fields_of("stratum", {"stratum_id", "notes"})
TABLE_FIELDS = fields_of("table", {"table_id", "page", "label", "caption_summary", "skipped_reason", "table_level_labels", "columns", "notes"})
LABEL_FIELDS = fields_of("table_level_labels", set())
COLUMN_FIELDS = fields_of("column", {"column_id", "notes"})
RECORD_FIELDS = fields_of("record", {"record_id", "notes"})

# Copied as printed, so compared character by character
EXACT_FIELDS = {"value_as_printed", "row_label_as_printed", "row_code_as_printed", "header_as_printed", "stratum_label_as_printed",
	"label_footnote_marker", "footnote_marker", "dispersion_as_printed", "rank_as_printed", "period_as_printed",
	"period_context_as_printed", "condition_as_printed", "condition_code_as_printed", "age_group_as_printed", "sex_as_printed"}
VALUE_FIELDS = {"value", "value_as_printed", "value_kind", "value_min", "value_max"}
MIN_RECORD_SCORE = 2.5


def norm(text):
	if text is None:
		return ""
	# Lists and dicts (stratum_ids, symbols, footnotes, field_pages) are compared as sorted JSON
	if isinstance(text, (dict, list)):
		text = json.dumps(text, sort_keys=True, ensure_ascii=False)
	text = unicodedata.normalize("NFKD", str(text))
	text = "".join(ch for ch in text if not unicodedata.combining(ch))
	text = text.lower().replace("±", " pm ")
	loose = re.sub(r"[^a-z0-9]+", " ", text).strip()
	# A text made only of symbols ('%', '—', '*') keeps them, or it would equal null
	return loose if loose else exact(text)


def exact(text):
	if text is None:
		return ""
	return re.sub(r"\s+", " ", unicodedata.normalize("NFC", str(text))).strip()


def norm_label(text):
	return re.sub(r"^(?:fig(?:ura)?|tab(?:ela)?)\b", lambda match: "figura" if match.group(0).startswith("f") else "tabela", norm(text))


def similarity(a, b):
	a, b = norm(a), norm(b)
	if a == b:
		return 1.0
	return difflib.SequenceMatcher(None, a, b).ratio()


def number_tokens(text):
	return set(re.findall(r"\d+(?:[.,]\d+)*", text or ""))


def field_differs(field, value_a, value_b):
	if isinstance(value_a, bool) or isinstance(value_b, bool) or isinstance(value_a, (int, float)) or isinstance(value_b, (int, float)):
		return value_a != value_b
	if field.split(".")[-1] in EXACT_FIELDS:
		return exact(value_a) != exact(value_b)
	return norm(value_a) != norm(value_b)


def prefix_flag(value_a, value_b):
	# One side cut short: the shorter text is the start of the longer one
	if not isinstance(value_a, str) or not isinstance(value_b, str):
		return ""
	text_a, text_b = norm(value_a), norm(value_b)
	if not text_a or not text_b or text_a == text_b:
		return ""
	if text_b.startswith(text_a):
		return "A_prefix_of_B"
	if text_a.startswith(text_b):
		return "B_prefix_of_A"
	return ""


def kind_of(field, value_a, value_b):
	field = field.split(".")[-1]
	if field in VALUE_FIELDS:
		return "value_mismatch"
	if value_a in (None, "", [], {}) or value_b in (None, "", [], {}):
		return "null_vs_text"
	if number_tokens(str(value_a)) != number_tokens(str(value_b)):
		return "numbers_differ"
	return "wording"


def greedy_ids(candidates):
	candidates.sort(key=lambda c: (-c[0], c[1], c[2]))
	new_id_for_b, used_a = {}, set()
	for score, id_a, id_b in candidates:
		if id_a in used_a or id_b in new_id_for_b:
			continue
		used_a.add(id_a)
		new_id_for_b[id_b] = id_a
	return new_id_for_b


def pair_strata(strata_a, strata_b):
	# Each A stratum takes the B stratum with the same label, dimension and parent label, best scores first. Returns {B id: A id}
	labels_a = {stratum["stratum_id"]: stratum.get("stratum_label_as_printed") for stratum in strata_a}
	labels_b = {stratum["stratum_id"]: stratum.get("stratum_label_as_printed") for stratum in strata_b}
	candidates = []
	for stratum_a in strata_a:
		for stratum_b in strata_b:
			score = 3.0 * similarity(stratum_a.get("stratum_label_as_printed"), stratum_b.get("stratum_label_as_printed"))
			score += 1.0 if stratum_a.get("stratum_dimension") == stratum_b.get("stratum_dimension") else 0.0
			score += 1.0 if norm(labels_a.get(stratum_a.get("parent_stratum_id"))) == norm(labels_b.get(stratum_b.get("parent_stratum_id"))) else 0.0
			# Change 10: 'Masc' and 'Masc.' are two strata (rule 6), so the exact label wins over the punctuation-free one
			score += 0.5 if exact(stratum_a.get("stratum_label_as_printed")) == exact(stratum_b.get("stratum_label_as_printed")) else 0.0
			score += 0.1 if stratum_a["stratum_id"] == stratum_b["stratum_id"] else 0.0
			if score >= 3.5:
				candidates.append((score, stratum_a["stratum_id"], stratum_b["stratum_id"]))
	return greedy_ids(candidates)


def mapped(new_id_for_b, old_id):
	if not old_id:
		return old_id
	return new_id_for_b.get(old_id, old_id + "?B")


def rewrite_b_ids(new_stratum_for_b, data_b):
	for stratum in data_b["strata"]:
		stratum["stratum_id"] = mapped(new_stratum_for_b, stratum["stratum_id"])
		stratum["parent_stratum_id"] = mapped(new_stratum_for_b, stratum.get("parent_stratum_id"))
	for table in data_b["tables"]:
		table["stratum_ids"] = [mapped(new_stratum_for_b, stratum_id) for stratum_id in table.get("stratum_ids") or []]
		for column in table.get("columns") or []:
			column["stratum_id"] = mapped(new_stratum_for_b, column.get("stratum_id"))
	for record in data_b["records"]:
		record["stratum_ids"] = [mapped(new_stratum_for_b, stratum_id) for stratum_id in record.get("stratum_ids") or []]


def cell_key(record):
	return (norm(record.get("row_label_as_printed")), exact(record.get("value_as_printed")))


def pair_columns(table_a, table_b, records_a, records_b):
	# Columns pair by the (row label, value) cells their records share, best overlap first, then by header
	def footprints(table, records):
		cells = {(column["column_id"], column.get("cell_part")): set() for column in table.get("columns") or []}
		for record in records:
			key = (record.get("column_id"), record.get("cell_part"))
			if record.get("table_id") == table["table_id"] and key in cells:
				cells[key].add(cell_key(record))
		return cells
	cells_a, cells_b = footprints(table_a, records_a), footprints(table_b, records_b)
	headers_b = {(column["column_id"], column.get("cell_part")): column.get("header_as_printed") for column in table_b.get("columns") or []}
	candidates = []
	for column_a in table_a.get("columns") or []:
		key_a = (column_a["column_id"], column_a.get("cell_part"))
		for key_b in cells_b:
			overlap = len(cells_a[key_a] & cells_b[key_b])
			header_score = similarity(column_a.get("header_as_printed"), headers_b[key_b])
			candidates.append((overlap, header_score, key_a == key_b, key_a, key_b))
	candidates.sort(key=lambda c: (-c[0], -c[1], not c[2], c[3], c[4]))
	pairs, used_b = {}, set()
	for overlap, header_score, bSameKey, key_a, key_b in candidates:
		if key_a in pairs or key_b in used_b:
			continue
		if overlap == 0 and header_score < 0.6:
			continue
		pairs[key_a] = key_b
		used_b.add(key_b)
	return pairs


def pair_tables(tables_a, tables_b):
	# (page, label) first, same kind first inside it. Returns {B table_id: A table_id}
	by_key_b = {}
	for table in tables_b:
		by_key_b.setdefault((table["page"], norm_label(table["label"])), []).append(table)
	new_table_for_b = {}
	# Same kind across the whole document first, so a statistical_tests block on one side does not take the text block
	# the other side paired by kind (rodriguez1984 p6: A k10 tests + k11 text, B one k11 text)
	for bSameKindPass in (True, False):
		for table_a in tables_a:
			if table_a["table_id"] in new_table_for_b.values():
				continue
			candidates = by_key_b.get((table_a["page"], norm_label(table_a["label"])), [])
			if bSameKindPass:
				candidates_for_pass = [table for table in candidates if table["kind"] == table_a["kind"]]
			else:
				candidates_for_pass = candidates
			if not candidates_for_pass:
				continue
			table_b = candidates_for_pass[0]
			candidates.remove(table_b)
			new_table_for_b[table_b["table_id"]] = table_a["table_id"]
	return new_table_for_b


HEADER = ["diff_id", "doc_id", "page", "table_or_figure", "kind", "field", "a_index", "b_index", "label_a", "label_b",
	"a_value", "b_value", "value_as_printed_a", "value_as_printed_b", "prefix", "match_score", "cascade_size", "cascade_a_ids", "cascade_b_ids"]
# Fields not compared between two text records (change 10): the inventory rows already say how the text blocks differ
TEXT_PAIR_SKIPPED = {"table_id", "row_index"}


def row(doc_id, page, table_or_figure, kind, field, a_index, b_index, label_a="", label_b="", value_a="", value_b="",
	printed_a="", printed_b="", score=""):
	def cell(value):
		if isinstance(value, (dict, list)):
			return json.dumps(value, ensure_ascii=False, sort_keys=True)
		return "" if value is None else value
	return [doc_id, page, table_or_figure, kind, field, a_index, b_index, label_a, label_b, cell(value_a), cell(value_b),
		cell(printed_a), cell(printed_b), prefix_flag(value_a, value_b), score, "", "", ""]


def collapse_cascades(keyed_rows):
	# One line per (A table, A column, cell part, field, value A, value B): a rule misread down a column is decided once
	# (change 10). keyed_rows is [(key, row, a id, b id)] in record order; a line alone keeps its blank cascade columns
	groups = {}
	for key, out_row, id_a, id_b in keyed_rows:
		groups.setdefault(key, []).append((out_row, id_a, id_b))
	rows = []
	for members in groups.values():
		first_row = members[0][0]
		if len(members) > 1:
			first_row[-3:] = [len(members), " ".join(id_a for _, id_a, _ in members), " ".join(id_b for _, _, id_b in members)]
		rows.append(first_row)
	return rows


def compare_tables(doc_id, data_a, data_b):
	rows = []
	tables_a, tables_b, records_a, records_b = data_a["tables"], data_b["tables"], data_a["records"], data_b["records"]
	new_table_for_b = pair_tables(tables_a, tables_b)
	tables_by_id_b = {table["table_id"]: table for table in tables_b}
	paired_b = {table_id_a: tables_by_id_b[table_id_b] for table_id_b, table_id_a in new_table_for_b.items()}
	new_column_for_b = {}
	for table_a in tables_a:
		table_b = paired_b.get(table_a["table_id"])
		if table_b is None:
			rows.append(row(doc_id, table_a["page"], table_a["label"], "only_in_A", "table", table_a["table_id"], ""))
			continue
		fields = [(field, table_a.get(field), table_b.get(field)) for field in TABLE_FIELDS]
		labels_a, labels_b = table_a.get("table_level_labels") or {}, table_b.get("table_level_labels") or {}
		fields += [("table_level_labels." + field, labels_a.get(field), labels_b.get(field)) for field in LABEL_FIELDS]
		column_pairs = pair_columns(table_a, table_b, records_a, records_b)
		columns_b = {(column["column_id"], column.get("cell_part")): column for column in table_b.get("columns") or []}
		for column_a in table_a.get("columns") or []:
			key_a = (column_a["column_id"], column_a.get("cell_part"))
			column_b = columns_b.pop(column_pairs.get(key_a), None)
			if column_b is None:
				rows.append(row(doc_id, table_a["page"], table_a["label"], "only_in_A", "column", table_a["table_id"] + "." + column_a["column_id"], ""))
				continue
			new_column_for_b[(table_b["table_id"], column_b["column_id"], column_b.get("cell_part"))] = column_a["column_id"]
			fields += [("columns.%s.%s" % (column_a["column_id"], field), column_a.get(field), column_b.get(field)) for field in COLUMN_FIELDS]
		for column_id, cell_part in columns_b:
			rows.append(row(doc_id, table_a["page"], table_a["label"], "only_in_B", "column", "", table_b["table_id"] + "." + column_id))
		for field, value_a, value_b in fields:
			if field_differs(field, value_a, value_b):
				rows.append(row(doc_id, table_a["page"], table_a["label"], kind_of(field, value_a, value_b), field,
					table_a["table_id"], table_b["table_id"], value_a=value_a, value_b=value_b))
	for table_b in tables_b:
		if table_b["table_id"] not in new_table_for_b:
			rows.append(row(doc_id, table_b["page"], table_b["label"], "only_in_B", "table", "", table_b["table_id"]))
	# B records take the A table and column ids, so they only flag a cell that really sits elsewhere
	for record in records_b:
		key = (record.get("table_id"), record.get("column_id"), record.get("cell_part"))
		if key in new_column_for_b:
			record["column_id"] = new_column_for_b[key]
		record["table_id"] = new_table_for_b.get(record.get("table_id"), str(record.get("table_id")) + "?B")
	return rows


def is_text(record):
	return norm(record.get("table_or_figure")) == "text"


def record_label(record):
	return " / ".join(str(part) for part in (record.get("row_label_as_printed"), record.get("column_id"), record.get("condition_as_printed")) if part)


def record_pair_score(a, b):
	if is_text(a) and is_text(b):
		# Rule 4: text records pair by the number, then by the words around it
		score = 3.0 if exact(a.get("value_as_printed")) == exact(b.get("value_as_printed")) else 0.0
		score += 1.0 * similarity(a.get("row_label_as_printed"), b.get("row_label_as_printed"))
		score += 0.5 if a.get("row_index") == b.get("row_index") else 0.0
		return score
	score = 3.0 * similarity(a.get("row_label_as_printed"), b.get("row_label_as_printed"))
	score += 0.5 if exact(a.get("row_label_as_printed")) == exact(b.get("row_label_as_printed")) else 0.0
	score += 1.0 if a.get("column_id") == b.get("column_id") else 0.0
	score += 0.5 if a.get("cell_part") == b.get("cell_part") else 0.0
	score += 1.0 if a.get("row_index") == b.get("row_index") else 0.0
	score += 0.5 if exact(a.get("value_as_printed")) == exact(b.get("value_as_printed")) else 0.0
	score += 1.0 if sorted(a.get("stratum_ids") or []) == sorted(b.get("stratum_ids") or []) else 0.0
	score += 0.5 if norm(a.get("period_as_printed")) == norm(b.get("period_as_printed")) else 0.0
	score += 1.0 * similarity(a.get("condition_as_printed"), b.get("condition_as_printed"))
	return score


def pair_in_groups(records_a, records_b, indexes_a, indexes_b, group_of):
	# Inside each group the best scores pair first, ties keep file order
	groups = {}
	for side, records, indexes in (("a", records_a, indexes_a), ("b", records_b, indexes_b)):
		for index in indexes:
			groups.setdefault(group_of(records[index]), {"a": [], "b": []})[side].append(index)
	pairs, only_a, only_b = [], [], []
	for key in sorted(groups):
		group_a, group_b = groups[key]["a"], groups[key]["b"]
		candidates = []
		for ia in group_a:
			for ib in group_b:
				score = record_pair_score(records_a[ia], records_b[ib])
				if score >= MIN_RECORD_SCORE:
					candidates.append((score, ia, ib))
		candidates.sort(key=lambda c: (-c[0], c[1], c[2]))
		used_a, used_b = set(), set()
		for score, ia, ib in candidates:
			if ia in used_a or ib in used_b:
				continue
			used_a.add(ia)
			used_b.add(ib)
			pairs.append((score, ia, ib))
		only_a += [ia for ia in group_a if ia not in used_a]
		only_b += [ib for ib in group_b if ib not in used_b]
	return pairs, only_a, only_b


def pair_records(records_a, records_b):
	# First inside (table, page); then the text records left alone pair across every text entry of their page (change 10:
	# A and B split the same text into different blocks)
	pairs, only_a, only_b = pair_in_groups(records_a, records_b, range(len(records_a)), range(len(records_b)),
		lambda record: (str(record.get("table_id")), record.get("page") or 0))
	text_a = [ia for ia in only_a if is_text(records_a[ia])]
	text_b = [ib for ib in only_b if is_text(records_b[ib])]
	text_pairs, text_only_a, text_only_b = pair_in_groups(records_a, records_b, text_a, text_b, lambda record: record.get("page") or 0)
	only_a = sorted(set(only_a) - set(text_a) | set(text_only_a))
	only_b = sorted(set(only_b) - set(text_b) | set(text_only_b))
	return sorted(pairs + text_pairs, key=lambda p: p[1]), only_a, only_b


def compare_strata(doc_id, strata_a, strata_b, original_b_ids):
	rows = []
	strata_by_id_b = {stratum["stratum_id"]: stratum for stratum in strata_b}
	for stratum_a in strata_a:
		stratum_b = strata_by_id_b.pop(stratum_a["stratum_id"], None)
		if stratum_b is None:
			rows.append(row(doc_id, "", "strata", "only_in_A", "stratum", stratum_a["stratum_id"], ""))
			continue
		for field in STRATUM_FIELDS:
			if field_differs(field, stratum_a.get(field), stratum_b.get(field)):
				rows.append(row(doc_id, "", "strata", kind_of(field, stratum_a.get(field), stratum_b.get(field)), field,
					stratum_a["stratum_id"], original_b_ids.get(stratum_b["stratum_id"], stratum_b["stratum_id"]),
					stratum_a.get("stratum_label_as_printed"), stratum_b.get("stratum_label_as_printed"), stratum_a.get(field), stratum_b.get(field)))
	for stratum_id in strata_by_id_b:
		rows.append(row(doc_id, "", "strata", "only_in_B", "stratum", "", original_b_ids.get(stratum_id, stratum_id)))
	return rows


def compare_document(name, root=ROOT):
	doc_id = name[:-5]
	with open(os.path.join(root, "A", name), encoding="utf-8") as handle:
		data_a = json.load(handle)
	with open(os.path.join(root, "B", name), encoding="utf-8") as handle:
		data_b = json.load(handle)
	rows = []
	for field in ("document_kind", "schema_version"):
		if data_a.get(field) != data_b.get(field):
			rows.append(row(doc_id, "", "document", "wording", field, "", "", value_a=data_a.get(field), value_b=data_b.get(field)))
	# Strata first, B ids rewritten to the paired A ids
	new_stratum_for_b = pair_strata(data_a["strata"], data_b["strata"])
	original_b_ids = {mapped(new_stratum_for_b, stratum["stratum_id"]): stratum["stratum_id"] for stratum in data_b["strata"]}
	rewrite_b_ids(new_stratum_for_b, data_b)
	rows += compare_strata(doc_id, data_a["strata"], data_b["strata"], original_b_ids)
	# Tables second (they rewrite the B table and column ids), then the records
	rows += compare_tables(doc_id, data_a, data_b)
	records_a, records_b = data_a["records"], data_b["records"]
	pairs, only_a, only_b = pair_records(records_a, records_b)
	keyed_rows = []
	for score, ia, ib in pairs:
		a, b = records_a[ia], records_b[ib]
		bTextPair = is_text(a) and is_text(b)
		for field in RECORD_FIELDS:
			if bTextPair and field in TEXT_PAIR_SKIPPED:
				continue
			if field_differs(field, a.get(field), b.get(field)):
				out_row = row(doc_id, a["page"], a["table_or_figure"], kind_of(field, a.get(field), b.get(field)), field,
					a["record_id"], b["record_id"], record_label(a), record_label(b), a.get(field), b.get(field),
					a.get("value_as_printed"), b.get("value_as_printed"), round(score, 2))
				cascade_key = (a.get("table_id"), a.get("column_id"), a.get("cell_part"), field,
					json.dumps(a.get(field), sort_keys=True, ensure_ascii=False), json.dumps(b.get(field), sort_keys=True, ensure_ascii=False))
				keyed_rows.append((cascade_key, out_row, a["record_id"], b["record_id"]))
	field_lines = len(keyed_rows)
	rows += collapse_cascades(keyed_rows)
	for ia in only_a:
		a = records_a[ia]
		rows.append(row(doc_id, a["page"], a["table_or_figure"], "only_in_A", "record", a["record_id"], "", record_label(a), "",
			printed_a=a.get("value_as_printed")))
	for ib in only_b:
		b = records_b[ib]
		rows.append(row(doc_id, b["page"], b["table_or_figure"], "only_in_B", "record", "", b["record_id"], "", record_label(b),
			printed_b=b.get("value_as_printed")))
	return rows, len(records_a), len(records_b), len(pairs), field_lines


def main(doc_ids, root=ROOT, out_dir=None):
	out_dir = out_dir or os.path.join(root, "method")
	os.makedirs(out_dir, exist_ok=True)
	if doc_ids:
		names = [doc_id + ".json" for doc_id in doc_ids]
		out_path = os.path.join(out_dir, "diff_%s.csv" % doc_ids[0]) if len(doc_ids) == 1 else os.path.join(out_dir, "diff_selected.csv")
	else:
		names = sorted(os.path.basename(p) for p in glob.glob(os.path.join(root, "A", "*.json")) if os.path.exists(os.path.join(root, "B", os.path.basename(p))))
		out_path = os.path.join(out_dir, "diff.csv")
	out_rows = []
	for name in names:
		rows, count_a, count_b, count_pairs, field_lines = compare_document(name, root)
		out_rows += rows
		print("%s: A records %d, B records %d, matched pairs %d, diff rows %d (record field differences %d before collapsing cascades)"
			% (name[:-5], count_a, count_b, count_pairs, len(rows), field_lines))
	with open(out_path, "w", encoding="utf-8", newline="") as handle:
		writer = csv.writer(handle)
		writer.writerow(HEADER)
		for number, out_row in enumerate(out_rows, 1):
			writer.writerow(["D%04d" % number] + out_row)
	print("wrote " + out_path)


def self_check():
	assert norm_label("Tab. 1") == norm_label("TABELA 1") and norm_label("FIG. 2") == norm_label("Fig. 2")
	# Printed text is exact, the rest loose; numbers and booleans exact
	assert field_differs("value_as_printed", "4,22", "4.22") and not field_differs("value_as_printed", "4,22 ", "4,22")
	assert not field_differs("measure_as_printed", "Prevalência", "prevalencia") and field_differs("rate_multiplier", 100, 1000)
	assert field_differs("is_estimate", True, False) and not field_differs("field_pages", {"a": 1, "b": 2}, {"b": 2, "a": 1})
	assert number_tokens("1.626.745 amostras") == {"1.626.745"}
	# A unit that is only a symbol still differs from null
	assert field_differs("unit_as_printed", "%", None) and not field_differs("unit_as_printed", "%", " % ")
	# The prefix flag names the side that was cut
	assert prefix_flag("Excluindo", "Excluindo São Paulo") == "A_prefix_of_B"
	assert prefix_flag("Estimativa de prevalência (por 100)", "Estimativa de prevalência") == "B_prefix_of_A" and prefix_flag("a", "a") == ""
	# Strata numbered in another order pair by label
	strata_a = [{"stratum_id": "s1", "parent_stratum_id": None, "stratum_dimension": "study", "stratum_label_as_printed": None},
		{"stratum_id": "s2", "parent_stratum_id": "s1", "stratum_dimension": "place", "stratum_label_as_printed": "NORTE"},
		{"stratum_id": "s3", "parent_stratum_id": "s2", "stratum_dimension": "place", "stratum_label_as_printed": "Acre"}]
	strata_b = [dict(strata_a[0]), dict(strata_a[2], stratum_id="s2", parent_stratum_id="s3"), dict(strata_a[1], stratum_id="s3")]
	assert pair_strata(strata_a, strata_b) == {"s1": "s1", "s2": "s3", "s3": "s2"}
	# Table records pair by row label and column; a misread value still pairs, a different row does not take its place
	records_a = [{"table_id": "k3", "page": 9, "table_or_figure": "TABELA I", "column_id": "c5", "cell_part": "whole", "row_index": 1,
		"row_label_as_printed": "Rondônia", "stratum_ids": ["s5"], "value_as_printed": "1,0"},
		{"table_id": "k3", "page": 9, "table_or_figure": "TABELA I", "column_id": "c5", "cell_part": "whole", "row_index": 2,
		"row_label_as_printed": "Acre", "stratum_ids": ["s6"], "value_as_printed": "2,4"}]
	records_b = [dict(records_a[1]), dict(records_a[0], value_as_printed="1,6")]
	pairs, only_a, only_b = pair_records(records_a, records_b)
	assert [(ia, ib) for score, ia, ib in pairs] == [(0, 1), (1, 0)] and only_a == [] and only_b == []
	# Text records pair by the number even when the line order differs; a number on one side only stays alone
	text_a = [{"table_id": "k2", "page": 8, "table_or_figure": "text", "row_index": 1, "row_label_as_printed": "prevalência de 4,22%", "value_as_printed": "4,22"}]
	text_b = [{"table_id": "k2", "page": 8, "table_or_figure": "text", "row_index": 1, "row_label_as_printed": "De um total de 1.626.745 amostras", "value_as_printed": "1.626.745"},
		{"table_id": "k2", "page": 8, "table_or_figure": "text", "row_index": 4, "row_label_as_printed": "uma prevalência de 4,22%", "value_as_printed": "4,22"}]
	pairs, only_a, only_b = pair_records(text_a, text_b)
	assert [(ia, ib) for score, ia, ib in pairs] == [(0, 1)] and only_b == [0]
	# Two text entries on one page against one: the same kind pairs first, the tests block stays alone
	tables_a = [{"table_id": "k10", "page": 6, "label": "text", "kind": "statistical_tests"}, {"table_id": "k11", "page": 6, "label": "text", "kind": "text"}]
	tables_b = [{"table_id": "k11", "page": 6, "label": "text", "kind": "text"}]
	assert pair_tables(tables_a, tables_b) == {"k11": "k11"}
	# Change 10: the exact label wins. A has 'Masc' and 'Masc.' as two strata, B the same two in the other order
	strata_a = [{"stratum_id": "s1", "parent_stratum_id": None, "stratum_dimension": "study", "stratum_label_as_printed": None},
		{"stratum_id": "s2", "parent_stratum_id": "s1", "stratum_dimension": "sex", "stratum_label_as_printed": "Masc"},
		{"stratum_id": "s3", "parent_stratum_id": "s1", "stratum_dimension": "sex", "stratum_label_as_printed": "Masc."}]
	strata_b = [dict(strata_a[0]), dict(strata_a[2], stratum_id="s2"), dict(strata_a[1], stratum_id="s3")]
	assert pair_strata(strata_a, strata_b) == {"s1": "s1", "s2": "s3", "s3": "s2"}
	# Change 10: text records pair by the number across two text entries of the same page
	text_a = [{"table_id": "k10", "page": 6, "table_or_figure": "text", "row_index": 1, "row_label_as_printed": "de 120 crianças vacinadas", "value_as_printed": "120"}]
	text_b = [{"table_id": "k11", "page": 6, "table_or_figure": "text", "row_index": 3, "row_label_as_printed": "de 120 crianças vacinadas", "value_as_printed": "120"}]
	pairs, only_a, only_b = pair_records(text_a, text_b)
	assert [(ia, ib) for score, ia, ib in pairs] == [(0, 0)] and not only_a and not only_b
	# Change 10: the same difference down a column is one line with every record; another column stays apart
	keyed_rows = [(("k1", "c2", "whole", "measure_as_printed", "a", "b"), row("d", 3, "Tabela 1", "wording", "measure_as_printed", "r%d" % number, "r%d" % number), "r%d" % number, "r%d" % number)
		for number in (1, 2, 3)]
	keyed_rows.append((("k1", "c3", "whole", "measure_as_printed", "a", "b"), row("d", 3, "Tabela 1", "wording", "measure_as_printed", "r4", "r4"), "r4", "r4"))
	collapsed = collapse_cascades(keyed_rows)
	assert len(collapsed) == 2 and collapsed[0][-3:] == [3, "r1 r2 r3", "r1 r2 r3"] and collapsed[1][-3:] == ["", "", ""]


def option(name, default=None):
	# '--root DIR' and '--out DIR'
	if name in sys.argv:
		return sys.argv[sys.argv.index(name) + 1]
	return default


if __name__ == "__main__":
	self_check()
	if "--check" not in sys.argv:
		root, out_dir = os.path.abspath(option("--root", ROOT)), option("--out")
		values = {option("--root"), option("--out")}
		main([arg for arg in sys.argv[1:] if not arg.startswith("--") and arg not in values], root, out_dir and os.path.abspath(out_dir))
