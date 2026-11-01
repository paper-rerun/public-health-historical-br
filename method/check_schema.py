# Check ../schema.json: the schema is valid, a two-record transcription (albuquerque1989 Tabela 1, 1960) passes and broken
# copies fail. Given files, validate each one against the schema, ignoring the adjudication provenance (origin,
# decision_ids, adjudicated_on, origin_rule)
# Usage: py -3.12 -I -X utf8 method/check_schema.py [file.json ...]   (no file: self-test only; exit code 1 when a file fails)
# Replaces saude-piloto/method/schema_selfcheck.py, whose example and broken copies are here
import copy
import json
import pathlib
import site
import sys

sys.path.append(site.getusersitepackages())
import jsonschema  # noqa: E402  lives in the user site-packages

SCHEMA_PATH = pathlib.Path(__file__).resolve().parent.parent / "schema.json"
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
VALIDATOR = jsonschema.Draft202012Validator(SCHEMA)
PROVENANCE_FIELDS = {"origin", "decision_ids", "adjudicated_on", "origin_rule"}


def WithoutProvenance(document):
	# The adjudicators add these at the top and on strata, tables and records
	cleaned = {key: value for key, value in document.items() if key not in PROVENANCE_FIELDS}
	for block in ("strata", "tables", "records"):
		if isinstance(cleaned.get(block), list):
			cleaned[block] = [{key: value for key, value in item.items() if key not in PROVENANCE_FIELDS} if isinstance(item, dict) else item
				for item in cleaned[block]]
	return cleaned


def Errors(document):
	return ["%s: %s" % ("/".join(str(part) for part in error.absolute_path), error.message[:200]) for error in VALIDATOR.iter_errors(document)]


def Stratum(stratum_id, parent, dimension, label, **fields):
	stratum = {field: None for field in SCHEMA["$defs"]["stratum"]["required"]}
	stratum.update({"stratum_id": stratum_id, "parent_stratum_id": parent, "stratum_dimension": dimension, "stratum_label_as_printed": label,
		"data_source_kind": "notification_records", "field_pages": {}})
	stratum.update(fields)
	return stratum


def Record(record_id, column_id, value, value_as_printed, stratum_ids):
	return {
		"record_id": record_id, "table_id": "k1", "column_id": column_id, "cell_part": "whole", "page": 3, "table_or_figure": "TABELA 1",
		"column_block": 1, "row_index": 1, "row_label_as_printed": "1960", "row_code_as_printed": None, "stratum_ids": stratum_ids,
		"period_as_printed": "1960", "period_context_as_printed": "1960 a 1985", "condition_as_printed": "hanseníase", "condition_code_as_printed": None,
		"measure_standardized": "detection_rate", "measure_as_printed": "coeficiente de detecção de casos", "value_kind": "numeric",
		"value": value, "value_min": None, "value_max": None, "value_as_printed": value_as_printed, "dispersion_as_printed": None,
		"rank_as_printed": None, "footnote_marker": None, "unit_as_printed": "por cem mil habitantes", "rate_multiplier_as_printed": "cem mil",
		"rate_multiplier": 100000, "rate_denominator_as_printed": "habitantes", "statistic": "rate_or_proportion", "is_estimate": False,
		"is_total": False, "total_kind": None, "data_source_kind": "notification_records", "cited_source_as_printed": None,
		"source_inconsistency": None, "notes": None,
	}


def Column(column_id, header, role, stratum_id):
	is_value = role == "value"
	return {
		"column_id": column_id, "column_block": 1, "cell_part": "whole", "header_as_printed": header, "role": role,
		"measure_standardized": "detection_rate" if is_value else None, "condition_as_printed": None,
		"unit_as_printed": "por cem mil habitantes" if is_value else None, "unit_source_place": "caption" if is_value else "not_applicable",
		"rate_multiplier_as_printed": "cem mil" if is_value else None, "rate_multiplier": 100000 if is_value else None,
		"rate_denominator_as_printed": "habitantes" if is_value else None, "statistic": "rate_or_proportion" if is_value else None,
		"is_estimate": False, "is_total_column": False, "period_as_printed": None,
		"period_status": "from_row" if is_value else "not_applicable", "stratum_id": stratum_id, "notes": None,
	}


def TinyDocument():
	doc_id = (SCHEMA["properties"]["doc_id"].get("enum") or ["albuquerque1989-hanseniase-recife-1960-1985"])[0]
	return {
		"doc_id": doc_id, "transcriber": "A", "schema_version": SCHEMA["version"], "document_kind": "surveillance_series",
		"strata": [
			Stratum("s1", None, "study", None, place_as_printed="Recife", place_kind="municipality", municipality="Recife", stateProvince="Estado de Pernambuco",
				period_as_printed="1960 e 1985", field_pages={"place_as_printed": 1, "period_as_printed": 1}),
			Stratum("s2", "s1", "sex", "Masc.", sex_as_printed="Masc.", sex_standardized="male"),
			Stratum("s3", "s1", "sex", "Fem.", sex_as_printed="Fem.", sex_standardized="female"),
		],
		"tables": [{
			"table_id": "k1", "page": 3, "label": "TABELA 1", "kind": "results", "caption_summary": "detection rate per 100,000 by sex, Recife 1960-1985",
			"printed_rotated": False, "stratum_ids": ["s2", "s3"], "data_cells": 2, "transcribed": 2, "skipped_cells": 0, "skipped_reason": None, "privacy_skip": False,
			"table_level_labels": {
				"row_axis": "periods", "row_axis_as_printed": "Anos", "column_axis": "sex", "layout": "single_block", "table_period_as_printed": "Recife, 1960 a 1985",
				"table_period_place": "caption", "unit_statement_as_printed": "por cem mil habitantes", "rate_base_statement_as_printed": "por cem mil habitantes",
				"quantity_meaning_as_printed": "coeficiente de detecção de casos de hanseníase", "case_definition_as_printed": None, "classification_as_printed": None,
				"dispersion_meaning_as_printed": None, "printed_totals": [], "heading_levels": [], "symbols": [], "footnotes": [], "source_lines": [],
				"data_source_kind": "notification_records", "source_inconsistency": None,
			},
			"columns": [Column("c1", "Anos", "row_label", None), Column("c2", "Sexo / Masc.", "value", "s2"), Column("c3", "Sexo / Fem.", "value", "s3")],
			"notes": None,
		}],
		# Rule 22, example (c): the caption repeats the study, so a cell by sex gives the sex stratum only
		"records": [Record("r1", "c2", 5.7, "5,7", ["s2"]), Record("r2", "c3", 5.3, "5,3", ["s3"])],
		"end_checklist": {
			"strata": [], "tables": [{"table_id": "k1", "data_cells": 2, "transcribed": 2, "skipped_cells": 0, "closes": True}],
			"rows": [], "totals": [], "columns": [], "markers": [], "symbols": [],
			"privacy": {"individual_case_lists": [], "personal_identifiers_written": 0}, "cited_data": [],
			"text_values": {"text_entries": 0, "text_records": 0, "text_values_repeating_tables": 0, "text_values_contradicting_tables": 0},
			"sums": {"tables": 1, "data_cells": 2, "transcribed": 2, "skipped_cells": 0, "records": 2, "strata": 3, "every_table_closes": True},
		},
	}


def SelfTest():
	jsonschema.Draft202012Validator.check_schema(SCHEMA)
	document = TinyDocument()
	assert not Errors(document), Errors(document)[:3]
	# Provenance is ignored, but only after it is taken off
	with_provenance = copy.deepcopy(document)
	with_provenance.update(adjudicated_on="2026-11-01", origin_rule="test")
	with_provenance["strata"][1].update(origin="A", decision_ids=["D0001"])
	with_provenance["records"][0].update(origin="both", decision_ids=["D0002"])
	assert Errors(with_provenance) and not Errors(WithoutProvenance(with_provenance))
	# A whole-study cell is ['s1']; an overall total (the rate of the whole) passes
	whole_study = copy.deepcopy(document)
	whole_study["records"][0].update(stratum_ids=["s1"], is_total=True, total_kind="overall", row_label_as_printed="Total")
	assert not Errors(whole_study), Errors(whole_study)[:3]
	broken_documents = {
		"statistic left to a default": ("statistic", None),
		"measure outside the closed list": ("measure_standardized", "coeficiente"),
		"s1 next to another stratum (change 1)": ("stratum_ids", ["s2", "s1"]),
		"a total without its kind (change 5)": ("is_total", True),
		"a kind on a cell that is not a total (change 5)": ("total_kind", "overall"),
		"a total kind outside the list": ("total_kind", "average"),
	}
	for reason, (field, new_value) in broken_documents.items():
		broken = copy.deepcopy(document)
		broken["records"][0][field] = new_value
		if field == "total_kind" and new_value == "average":
			broken["records"][0]["is_total"] = True
		assert Errors(broken), reason + " was accepted"
	broken = copy.deepcopy(document)
	broken["end_checklist"]["privacy"]["personal_identifiers_written"] = 1
	assert Errors(broken), "a personal identifier was accepted"
	# The pilot's version string fails: a 1.0 file is not a 2.0 file
	assert Errors(dict(document, schema_version="saude-1.0-pilot"))
	print("self-test ok: schema %s valid, %d rules, %d record fields; tiny transcription passes, %d broken ones fail"
		% (SCHEMA["version"], len(SCHEMA["rules"]), len(SCHEMA["$defs"]["record"]["required"]), len(broken_documents) + 2))


if __name__ == "__main__":
	SelfTest()
	failed = 0
	for path in sys.argv[1:]:
		errors = Errors(WithoutProvenance(json.loads(pathlib.Path(path).read_text(encoding="utf-8"))))
		print("%s: %s" % (path, "ok" if not errors else "%d errors" % len(errors)))
		for error in errors[:20]:
			print("  " + error)
		failed += bool(errors)
	sys.exit(1 if failed else 0)
