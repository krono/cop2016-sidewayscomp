#!/usr/bin/env make -f
BASE=cop2016-sidewayscomp
BIB=references.bib

LATEX=pdflatex $(LATEXOPTS)
BIBTEX=biber

#############################################################################
TEXFILE=$(BASE).tex
PDF=$(BASE).pdf
BIBOUT=$(BASE).bbl
AUXOUT=$(BASE).aux
TO_CLEAN=$(BASE).aux $(BASE).log $(BASE).out $(BASE).pdf $(BASE).tdo \
	$(BASE).toc $(BASE).bbl $(BASE).blg $(BASE).bcf $(BASE).run.xml \
	$(BASE).synctex.gz
LATEXOPTS=-synctex=1
#############################################################################

.SECONDARY: $(AUXOUT) $(BIBOUT)

.PHONY : all
all: $(PDF)

.PHONY : clean
clean :
	rm -f $(TO_CLEAN) *.log

%.pdf: %.tex %.aux %.bbl
	@echo "TeXing for pdf"
	@$(LATEX) $<
	@while grep -q "Rerun to get cross-references right" \
	$(BASE).log ; do \
	    echo " again..." ; \
	    $(LATEX) $< ; \
	done

%.bbl: $(BIB)
	@echo "BibTeXing"
	@rm -f $(PDF)
	@$(BIBTEX) $(BASE)

%.aux:
	@echo "TeXing for aux"
	@$(LATEX) $(BASE)
