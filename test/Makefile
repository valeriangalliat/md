MD = $(PWD)/../bin/md

all:
	@echo ':: Take input from `stdin`, finds title, use default layout'
	cat test.md | $(MD) | diff test.html -
	@echo

	@echo ':: Take input as argument, finds title, use default layout'
	$(MD) test.md | diff test.html -
	@echo

	@echo ':: Take title from the front matter'
	$(MD) title.md | diff title.html -
	@echo

	@echo ':: Take config file as argument'
	$(MD) --config config config.md | diff config.html -
	@echo

	@echo ':: Allow to define and configure extensions'
	$(MD) extensions.md | diff extensions.html -
	@echo

	@echo ':: Find `.mdrc` relative to file, use custom layout'
	$(MD) mdrc/test.md | diff mdrc/test.html -
	@echo

	@echo ':: Merge parent `.mdrc`, layout relative to final `.mdrc`'
	$(MD) mdrc/nested/test.md | diff mdrc/nested/test.html -
	@echo

	@echo ':: Merge Markdown meta-data with `.mdrc` and resolve layout'
	$(MD) mdrc/layout/test.md | diff mdrc/layout/test.html -
	@echo

	@echo ':: Do not extend if specified'
	$(MD) mdrc/extend/test.md | diff mdrc/extend/test.html -
	@echo
