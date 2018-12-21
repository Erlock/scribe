run:
	pipenv run python3 src/main.py

test:
	pipenv run python3 src/detect.py ${input}

c6:
	pipenv run python3 src/spectral_analysis.py ${input}

onset:
	pipenv run python3 src/time_domain.py

test-env:
	pipenv run python3 tests/test.py
