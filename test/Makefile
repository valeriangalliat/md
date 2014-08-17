MD = $(PWD)/../md

all: real-all

ALL += input-stdin
input-stdin:
	@echo ':: Take input from `stdin`, finds title, use default layout'
	cat test.md | $(MD) | diff test-expected.html -
	@echo

ALL += input-arg
input-arg:
	@echo ':: Take input as argument, finds title, use default layout'
	$(MD) test.md | diff test-expected.html -
	@echo

ALL += title-matter
title-matter:
	@echo ':: Take title from the front matter'
	$(MD) title.md | diff title-expected.html -
	@echo

ALL += config
config: force
	@echo ':: Take config file as argument'
	$(MD) --config config config.md | diff config-expected.html -
	@echo

ALL += mdconfig
mdconfig: force
	@echo ':: Find `.mdconfig` relative to file, use custom layout'
	$(MD) mdconfig/test.md | diff mdconfig/test-expected.html -
	@echo

	@echo ':: Merge parent `.mdconfig`, layout relative to final `.mdconfig`'
	$(MD) mdconfig/nested/test.md | diff mdconfig/nested/test-expected.html -
	@echo

ALL += layout
layout: force
	@echo ':: Layout defined in Markdown'
	$(MD) layout/test.md | diff layout/test-expected.html -
	@echo

real-all: $(ALL)

force:
