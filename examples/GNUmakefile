MD = ../md

MARKDOWNS = $(shell find . -name '*.md')
HTMLS = ${MARKDOWNS:.md=.html}

all: $(HTMLS)

%.html: %.md
	$(MD) $< > $@
