test:
	python test_cases.py
coverage:
	export DJANGO_SETTINGS_MODULE=geoip.test_settings && \
	coverage report --omit="antigate/test*"
sphinx:
	cd docs && sphinx-build -b html -d .build/doctrees . .build/html

pep8:
	@flake8 antigate --ignore=E402,E731,F401,F401 --exclude=migrations,south_migrations

clean:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

release: clean
	@python setup.py register sdist upload --sign
	@python setup.py bdist_wheel upload --sign