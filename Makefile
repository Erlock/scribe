test:
	PYTHONPATH=${PWD} pipenv run python3 tests/detect.py

test-env:
	PYTHONPATH=${PWD} pipenv run python3 tests/test.py
