test:
	python test_cases.py

coverage:
	coverage run --branch --source=antigate test_cases.py
	coverage report --omit="test*"

sphinx:
	@rm -rf ./docs/.build/html/
	@cd docs && sphinx-build -b html -d .build/doctrees . .build/html
	@xdg-open docs/.build/html/index.html >& /dev/null || open docs/.build/html/index.html >& /dev/null || true

pep8:
	@flake8 antigate

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
