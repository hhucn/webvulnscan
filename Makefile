test:
	flake8 .
	nosetests test --verbose --with-coverage --cover-package=webvulnscan --cover-min-percentage=50

.PHONY: test

