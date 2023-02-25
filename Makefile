format:
	black .
	ruff . --fix

lint:
	black . --check
	ruff .
