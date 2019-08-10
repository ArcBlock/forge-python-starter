TOP_DIR=.
README=$(TOP_DIR)/README.md

VERSION=$(strip $(shell cat version))

init:
	@echo "Install software required for this repo..."
	@npm install -g yarn
	@yarn install

create-env:
	@pip install virtualenv
	@pip install virtualenvwrapper
	( \
		source /usr/local/bin/virtualenvwrapper.sh; \
		mkvirtualenv -p python3 forge-env; \
		pip install -r requirements.txt; \
	)

install:
	@pip3 install -r requirements.txt

run-client:
	@echo "Running the client..."
	@yarn start:client

run-server:
	@echo "starting server..."
	( \
		source /usr/local/bin/virtualenvwrapper.sh; \
		workon forge-env; \
		python server/app.py; \
	)

declare:
	@node tools/declare.js

include .makefiles/*.mk

.PHONY: build init travis-init install dep pre-build post-build all test doc precommit travis clean watch run bump-version create-pr
