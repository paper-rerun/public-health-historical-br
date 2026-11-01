# The 15-word cap, checked by script (saude-piloto/RODADA.md, change 12). The adjudicator runs it on its own output before
# closing a document: every string in adjudicated/<doc_id>.json and every cell of adjudicated/<doc_id>_decisions.csv is
# searched for a run of more than 15 words found in the PDF text layer, and for a quotation longer than 15 words. merge.py
# imports the same functions and runs the same search over the merged files
# Usage: py -3.12 -I -X utf8 method/check_long_copies.py doc_id [doc_id ...] [--root DIR]   (exit code 1 when anything is found)
# --root: the round folder with sources.json, pdfs and adjudicated/ (default: the folder above this script)
# Limit: a scanned page without a text layer (the tables of the Revista de Saúde Pública) cannot be searched for copies;
# only the quotation marks are checked there
import ast
import csv
import json
import os
import re
import subprocess
import sys

MAX_QUOTE_WORDS = 15
# Quotes: 'x', "x", ‘x’, “x”. The single quote must not touch a letter, so "B's" is not a quote
QUOTE_PATTERN = re.compile(r"(?<![\w])'([^']{3,}?)'(?![\w])|\"([^\"]{3,}?)\"|‘([^’]+)’|“([^”]+)”")
# Ids and bookkeeping, never source text
NOT_SOURCE_KEYS = {"doc_id", "transcriber", "schema_version", "document_kind", "record_id", "table_id", "column_id", "stratum_id",
	"parent_stratum_id", "stratum_ids", "decision_ids", "origin", "adjudicated_on", "diff_id", "a_index", "b_index", "cascade_a_ids", "cascade_b_ids"}


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


def JsonHits(value, pdf_shingles, path=""):
	# (path, copy) for every string of the adjudicated file, keys in NOT_SOURCE_KEYS skipped
	hits = []
	if isinstance(value, dict):
		for key, each_value in value.items():
			if key not in NOT_SOURCE_KEYS:
				hits += JsonHits(each_value, pdf_shingles, f"{path}/{key}")
	elif isinstance(value, list):
		for index, each_value in enumerate(value):
			hits += JsonHits(each_value, pdf_shingles, f"{path}/{index}")
	elif isinstance(value, str):
		hits += [(path, copy) for copy in FindLongCopies(value, pdf_shingles)]
	return hits


def SelfCheck():
	# A 16-word copy is caught, a 15-word copy is not, and a 16-word quote is caught even when it is not in the PDF
	test_words = [f"w{index}" for index in range(30)]
	test_shingles = {tuple(test_words[index:index + MAX_QUOTE_WORDS + 1]) for index in range(len(test_words) - MAX_QUOTE_WORDS)}
	assert CopiedRuns(" ".join(test_words[:16]) + " x", test_shingles) == [" ".join(test_words[:16])]
	assert CopiedRuns(" ".join(test_words[:15]) + " x", test_shingles) == []
	assert LongQuotes("as in '" + " ".join(["z"] * 16) + "' here") and not LongQuotes("B's and '" + " ".join(["z"] * 15) + "'")
	# A dict repr with a long string of our own words is not a quote, but a long quote inside one of its strings still is
	assert not FindLongCopies(repr({"notes": " ".join(["z"] * 16)}), set())
	assert FindLongCopies(repr({"notes": "p3 says '" + " ".join(["z"] * 16) + "'"}), set())
	# In the adjudicated file, ids are skipped and the path names the field
	assert JsonHits({"records": [{"record_id": "r1", "notes": "'" + " ".join(["z"] * 16) + "'"}]}, set()) == [("/records/0/notes", " ".join(["z"] * 16))]


def Option(name, default=None):
	if name in sys.argv:
		return os.path.abspath(sys.argv[sys.argv.index(name) + 1])
	return default


if __name__ == "__main__":
	SelfCheck()
	root = Option("--root", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	option_values = {sys.argv[sys.argv.index("--root") + 1]} if "--root" in sys.argv else set()
	doc_ids = [arg for arg in sys.argv[1:] if not arg.startswith("--") and arg not in option_values]
	documents_by_id = {document["id"]: document for document in json.load(open(os.path.join(root, "sources.json"), encoding="utf-8"))["documents"]}
	found = 0
	for doc_id in doc_ids:
		pdf_shingles = LoadPdfWordShingles(os.path.join(root, documents_by_id[doc_id]["pdf_path"]))
		hits = JsonHits(json.load(open(os.path.join(root, "adjudicated", doc_id + ".json"), encoding="utf-8")), pdf_shingles)
		decisions_path = os.path.join(root, "adjudicated", doc_id + "_decisions.csv")
		if os.path.exists(decisions_path):
			for decision in csv.DictReader(open(decisions_path, encoding="utf-8-sig", newline="")):
				for column, text in decision.items():
					if column not in NOT_SOURCE_KEYS:
						hits += [(f"decisions {decision.get('diff_id')} {column}", copy) for copy in FindLongCopies(text, pdf_shingles)]
		print(f"{doc_id}: {len(hits)} copies or quotes over {MAX_QUOTE_WORDS} words")
		for where, copy in hits:
			print(f"  {where}: {copy[:160]}")
		found += len(hits)
	sys.exit(1 if found else 0)
