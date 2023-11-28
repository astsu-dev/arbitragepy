fmt:
		ruff check arbitragepy tests --fix
lint:
		ruff check arbitragepy tests
test:
		pytest -vvv tests
