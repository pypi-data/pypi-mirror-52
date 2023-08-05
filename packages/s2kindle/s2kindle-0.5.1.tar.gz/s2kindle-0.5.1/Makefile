PIPENV=PIPENV_VENV_IN_PROJECT=1 pipenv
PIPENV_RUN=$(PIPENV) run
SOURCES_FOLDER=./send_to_kindle
SOURCE_FILES=$(shell find . -name '*.py' -not -path **/.venv/*)
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
HASH := $(shell git rev-parse HEAD)
TAG := $(shell git tag -l --contains HEAD)

OSFLAG 				:=
ifeq ($(OS),Windows_NT)
	OSFLAG = WIN
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		OSFLAG = LINUX
	endif
	ifeq ($(UNAME_S),Darwin)
		OSFLAG = OSX
	endif
endif

check_on_master:
ifeq ($(BRANCH),master)
	echo "You are good to go!"
else
	$(error You are not in the master branch)
endif

env:
	$(PIPENV) install --dev

unit_test:
	PYTHONPATH=. $(PIPENV_RUN) pytest -vvv --cov=$(SOURCES_FOLDER) --cov-fail-under=90 --cov-report=html tests/unit

integration_test:
	PYTHONPATH=. $(PIPENV_RUN) pytest -vvv --cov=$(SOURCES_FOLDER) --cov-report=html tests/integration

format:
	$(PIPENV_RUN) isort -rc $(SOURCES_FOLDER)
	$(PIPENV_RUN) black $(SOURCE_FILES)

lint:
	$(PIPENV_RUN) bandit -r $(SOURCES_FOLDER)
	$(PIPENV_RUN) isort -rc $(SOURCES_FOLDER) --check-only
	$(PIPENV_RUN) black $(SOURCE_FILES) --check
	$(PIPENV_RUN) pylint $(SOURCES_FOLDER)

kindlegen:
	echo "See this website: https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211"
ifeq ($(OSFLAG),OSX)
	wget -O kindlegen.zip http://kindlegen.s3.amazonaws.com/KindleGen_Mac_i386_v2_9.zip
	unzip kindlegen.zip -d kindlegen
endif
ifeq ($(OSFLAG),LINUX)
	wget -O kindlegen.tar.gz http://kindlegen.s3.amazonaws.com/kindlegen_linux_2.6_i386_v2_9.tar.gz
endif

dists: check_on_master requirements sdist bdist wheels

requirements:
	pipenv run pipenv_to_requirements -f

sdist: requirements
	pipenv run python setup.py sdist

bdist: requirements
	pipenv run python setup.py bdist

wheels: requirements
	pipenv run python setup.py bdist_wheel

patch: check_on_master
	pipenv run bumpversion patch --verbose
	git push --follow-tags

minor: check_on_master
	pipenv run bumpversion minor --verbose
	git push --follow-tags

major: check_on_master
	pipenv run bumpversion major --verbose
	git push --follow-tags

pypi: sdist
ifeq ($(TAG),)
	@echo "Skipping PyPi publishing"
else
	CURRENT_TAG=$(TAG) pipenv run python setup.py verify
	pipenv run twine upload dist/*
endif

clean: clean-py clean-build clean-kindlegen clean-test

clean-test:
	rm -rf htmlcov

clean-py: 
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-build: 
	rm -fr dist/
	rm -fr build/
	rm -fr .eggs/
	rm -f requirements*.txt
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-kindlegen:
	rm -rf kindlegen/
	find . -name 'kindlegen.zip' -exec rm -f {} +
