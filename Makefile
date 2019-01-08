run:
	pipenv run python3 src/main.py

test:
	pipenv run python3 src/detect.py ${input}

plot-note:
	pipenv run python3 src/spectral_analysis.py ${input} ${note} ${octave}

onset:
	pipenv run python3 src/time_domain.py

test-env:
	pipenv run python3 tests/test.py
