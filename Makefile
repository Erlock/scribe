run:
	pipenv run python3 main.py

test:
	pipenv run python3 tests/detect.py

c6:
	pipenv run python3 tests/spectral_analysis.py ${input}

onset:
	pipenv run python3 tests/time_domain.py

test-env:
	pipenv run python3 tests/test.py
