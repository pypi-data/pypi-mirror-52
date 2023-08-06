SRC_DIRS = bluejay

##@ bootup

.PHONY: install
install: ## Installs missing dependencies with flit
install: flit-install pyenv-rehash

flit-install:
	flit install --pth-file

pyenv-rehash:
	@# as we don't use pip, we have to manually rehash the environment.
	command -v pyenv && pyenv rehash ||:

##@ Code Checks

.PHONY: test
test: ## Runs all the tests
test:
	python -m pytest tests

.PHONY: fixlint autofix
fixlint: autofix
autofix: ## Attempts to rectify any linting issues
autofix:
	autoflake --in-place --remove-unused-variables --recursive $(SRC_DIRS) tests
	isort --recursive $(SRC_DIRS) tests
	black $(SRC_DIRS) tests

.PHONY: lint
lint: ## Checks the code for any style violations
lint:
	autoflake --check --remove-unused-variables --recursive $(SRC_DIRS) tests
	isort --check-only --recursive $(SRC_DIRS) tests
	black --check $(SRC_DIRS) tests
	@# don't run mypy on the tests, since it doesn't work well with pytest yet
	mypy $(SRC_DIRS)

##@ Publishing

# We default to the Test PyPI, to avoid publishing accidentally.
PYPI_INDEX_NAME ?= testpypi

publish:
	flit --repository  '$(PYPI_INDEX_NAME)' publish
