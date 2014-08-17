MD = $(PWD)/../md

all:
	@echo ':: Take input from `stdin`, finds title, use default layout'
	cat test.md | $(MD) | diff test-expected.html -
	@echo

	@echo ':: Take input as argument, finds title, use default layout'
	$(MD) test.md | diff test-expected.html -
	@echo

	@echo ':: Take title from the front matter'
	$(MD) title.md | diff title-expected.html -
	@echo

	@echo ':: Take config file as argument'
	$(MD) --config config config.md | diff config-expected.html -
	@echo

	@echo ':: Find `.mdconfig` relative to file, use custom layout'
	$(MD) mdconfig/test.md | diff mdconfig/test-expected.html -
	@echo

	@echo ':: Merge parent `.mdconfig`, layout relative to final `.mdconfig`'
	$(MD) mdconfig/nested/test.md | diff mdconfig/nested/test-expected.html -
	@echo

	@echo ':: Merge Markdown meta-data with `.mdconfig` and resolve layout'
	$(MD) mdconfig/layout/test.md | diff mdconfig/layout/test-expected.html -
	@echo

	@echo ':: Do not extend if specified'
	$(MD) mdconfig/extend/test.md | diff mdconfig/extend/test-expected.html -
	@echo
