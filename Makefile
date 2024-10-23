PROJECT:= driviz
TESTS:= tests

.PHONY: check test codestyle docstyle lint pip

check: format lint

format:
	poetry run ruff format $(PROJECT) tests
	poetry run ruff check --fix --unsafe-fixes $(PROJECT) $(TESTS)

lint:
	poetry run ruff format --check $(PROJECT) $(TESTS)
	poetry run ruff check $(PROJECT) $(TESTS)
	poetry run mypy $(PROJECT)

lock:
	poetry lock --no-update

test:
	poetry run pytest --cov --cov-report=html --cov-report=xml

test-unit:
	poetry run pytest --cov --cov-report=html --cov-report=xml -m "not integration"

test-integration:
	poetry run pytest -m "integration"

--setup-poetry:
	@echo "Checking if Poetry is installed ..."; \
		poetry_path=$$(command -v "poetry"); \
		if [ -z "$${poetry_path}" ]; \
		then \
			echo "ERROR: Poetry not found.\
			\n  You should have Poetry installed in order to setup this project.\
			\n  https://python-poetry.org/docs/#installation\n"; \
			exit 1; \
		fi
	@echo "Checking if poetry.lock is up-to-date ..."; \
		lock_status=$$(poetry check --lock | grep " "); \
		if [ "$${lock_status}" != "All set!" ]; \
		then \
			poetry lock --no-update; \
			poetry install --sync; \
			poetry run pre-commit install --install-hooks; \
			git add poetry.lock; \
  			poetry run pre-commit run --files poetry.lock || true; \
  			git commit poetry.lock -m ":lock: Lock the project dependencies."; \
		else \
			echo "Poetry lock file is up-to-date."; \
			poetry install --sync; \
			poetry run pre-commit install --install-hooks; \
		fi

setup:
	@make -- --setup-poetry || exit 1;
	@echo "Checking pre-commits ..."; poetry run pre-commit run --all-files || exit 1
	@poetry_env_path=$$(poetry env info --path); echo "Setup is done!\nVirtual environment located at: $${poetry_env_path}"; exit 0
