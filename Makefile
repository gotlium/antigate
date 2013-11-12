test:
	python test_cases.py
coverage:
	export DJANGO_SETTINGS_MODULE=geoip.test_settings && \
	coverage report --omit="antigate/test*"
sphinx:
	cd docs && sphinx-build -b html -d .build/doctrees . .build/html
