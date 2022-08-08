
SERVICE_NAME=aqara_capi
IMAGE_NAME=${SERVICE_NAME}
TEST_IMAGE_NAME=${IMAGE_NAME}:test
PROD_IMAGE_NAME=${IMAGE_NAME}:prod
MYPY_FLAGS=--namespace-packages \
	--ignore-missing-imports \
	--no-implicit-reexport \
	--python-version 3.10 \
	--warn-unreachable \
	--warn-redundant-casts \
	--warn-incomplete-stub \
	--no-warn-no-return \
	--no-implicit-optional \
	--disallow-untyped-defs \
	--disallow-untyped-calls \
	--check-untyped-defs \
	--strict-equality \
	--disallow-untyped-decorators \
	--disallow-incomplete-defs \
	--disallow-any-generics \
	--show-error-codes \
	--pretty \
	--follow-imports=normal \
	--allow-redefinition \
	--no-incremental


isort:
	isort ${SERVICE_NAME} -w 120 -m 5 -j 4

mypy:
	python -m mypy ${SERVICE_NAME} ${MYPY_FLAGS}

flake8:
	python -m flake8 ${SERVICE_NAME} --max-line-length 120

pylint:
	python -m pylint ${SERVICE_NAME} --rcfile=ci/.pylint.cfg


fmt: isort

lint: mypy pylint flake8
	echo "Tests passed!"

build:
	python setup.py bdist_wheel --universal

clear:
	rm -rf build dist/*

push:
	twine upload dist/*

