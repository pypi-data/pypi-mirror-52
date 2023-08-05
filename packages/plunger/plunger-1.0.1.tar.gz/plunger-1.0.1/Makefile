NAME:=$(shell basename `pwd`)
PACKAGE:=$(shell echo $(NAME) | sed -e 's/-/_/g')
SCRIPT=$(NAME)

venv:
	python3 -m venv venv
	./venv/bin/pip install -U pip
	./venv/bin/pip install wheel
	./venv/bin/pip install -r requirements.txt

freeze: clean venv
	venv/bin/pip install -Ue .
	venv/bin/pip freeze | sed -e 's/-e .*/-e ./' \
		| grep -v pkg-resources \
		> requirements.txt

release:
	# zest.releaser must be installed somewhere in your PATH
	fullrelease

clean:
	rm -rf venv *.egg-info pip-selfcheck.json .Python .coverage .pytest_cache */__pycache__
