include common.mk

MD = ../md

MARKDOWNS = $(shell $(MARKDOWNS_COMMAND))
HTMLS = ${MARKDOWNS:.md=.html}

all: $(HTMLS)

%.html: %.md
	$(MD) $< > $@
