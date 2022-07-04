fmt:
		black arbitragepy tests
		isort arbitragepy tests
test:
		pytest -vvv tests
