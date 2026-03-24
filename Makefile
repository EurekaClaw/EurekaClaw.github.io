# Makefile for EurekaClaw documentation (Sphinx)

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build

.PHONY: help html html-zh clean livehtml livehtml-zh install

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

install:
	pip install -r requirements.txt

html:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)/zh" "$(BUILDDIR)/html/zh" $(SPHINXOPTS) $(O)
	@sed -i 's/window\.Stemmer = ChineseStemmer/window.Stemmer = EnglishStemmer/' "$(BUILDDIR)/html/zh/_static/language_data.js"
	@echo
	@echo "Build finished."
	@echo "  English: _build/html/index.html"
	@echo "  Chinese: _build/html/zh/index.html"

html-zh:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)/zh" "$(BUILDDIR)/html/zh" $(SPHINXOPTS) $(O)
	@sed -i 's/window\.Stemmer = ChineseStemmer/window.Stemmer = EnglishStemmer/' "$(BUILDDIR)/html/zh/_static/language_data.js"
	@echo
	@echo "Build finished. Open _build/html/zh/index.html"

livehtml:
	@echo "Proxy:   http://127.0.0.1:8000"
	@echo "English: http://127.0.0.1:8000/"
	@echo "Chinese: http://127.0.0.1:8000/zh/"
	@trap 'kill 0' EXIT; \
	 sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" --port 8002 $(SPHINXOPTS) $(O) & \
	 sphinx-autobuild "$(SOURCEDIR)/zh" "$(BUILDDIR)/html/zh" --port 8001 $(SPHINXOPTS) $(O) & \
	 python proxy.py & \
	 wait

livehtml-zh:
	sphinx-autobuild "$(SOURCEDIR)/zh" "$(BUILDDIR)/html/zh" $(SPHINXOPTS) $(O)

clean:
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
