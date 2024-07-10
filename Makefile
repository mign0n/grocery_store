WORKDIR = grocery_store
DEVREQS = dev-requirements.txt
REQS = requirements.txt

deps:
	pip install --upgrade pip pip-tools
	pip-compile --output-file $(REQS) --resolver=backtracking pyproject.toml

dev-deps: deps
	pip-compile --extra=dev --output-file $(DEVREQS) --resolver=backtracking pyproject.toml

install-deps: deps
	pip-sync $(REQS)

install-dev-deps: install-deps dev-deps
	pip-sync $(DEVREQS)

style:
	black $(WORKDIR)
	isort $(WORKDIR)
	flake8 --toml-config=pyproject.toml $(WORKDIR)
	mypy --config-file=pyproject.toml $(WORKDIR)
	pymarkdown scan .
