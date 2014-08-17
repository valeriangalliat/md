all: lint test

lint:
	pep8 md

test: force
	$(MAKE) -C $@

force:
