.PHONY: install run debug clean lint lint-strict

install:
	poetry install

run:
	poetry run python3 pac-man.py config.json

debug:
	poetry run python3 -m pdb pac-man.py config.json

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "poetry.lock" -exec rm -rf {} \;

lint:
	flake8
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8
	mypy . --strict
