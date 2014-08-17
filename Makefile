all: lint test

lint:
	pep8 md

test: force
	cd $@ && $(MAKE)

force:
