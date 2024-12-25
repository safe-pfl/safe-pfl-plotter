install-local:
	pip install .

upgrade-local:
	pip install --upgrade .

uninstall:
	pip uninstall safe-pfl-distance

check:
	python setup.py check

clean:
	@echo "cleaning"
	@rm -rf ./build
	@rm -rf ./dist
	@rm -rf ./*.egg-info

increment-version:
	@bump

source-distribution: clean
	@echo "building"
	@python setup.py sdist
	@python setup.py bdist_wheel --universal

sign:
	@echo "signing with gpg"
	@gpg --detach-sign -a dist/safe_pfl_plotter-*

publish-test: increment-version source-distribution sign
	@echo "test publishing"
	@twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose

publish: check source-distribution sign
	@echo "test publishing"
	@twine upload dist/* --verbose

install-test:
	pip install --index-url https://test.pypi.org/simple/ safe-pfl-distance --user

install:
	pip install safe-pfl-distance --user

download:
	pip download safe-pfl-distance

download-clean:
	pip download --no-deps safe-pfl-distance

doc-generate:
	@cd docs && make clean && make html