include common.mk

MARKDOWNS = $(shell $(MARKDOWNS_COMMAND))
HTMLS = ${MARKDOWNS:.md=.html}

all: $(HTMLS)

%.html: %.md
	$(MD) $< > $@
