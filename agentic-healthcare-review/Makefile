.PHONY: all references search test validate
all:
	python3 scripts/make_figures.py
	python3 scripts/build_pdfs.py
references:
	python3 scripts/resolve_references.py
search:
	python3 scripts/search_literature.py
test:
	python3 scripts/run_tests.py
validate:
	python3 scripts/validate_package.py
