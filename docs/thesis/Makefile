.PHONY: proof clean all

TARGETS = main
BIBFILES = $(wildcard *.bib)
TEXFILES = $(shell fd .tex)
FIGURES = $(wildcard figures/*.pdf figures/*.tex)
GENPDFS = $(patsubst %.svg,%.pdf,$(wildcard figures/*.svg))
PDFS = $(patsubst %,%.pdf,$(TARGETS))

all: $(PDFS)

%.pdf: %.tex $(TEXFILES) $(FIGURES) $(BIBFILES)
	latexmk -xelatex -shell-escape -bibtex $(basename $<)

%.pdf: %.svg
	inkscape --export-filename=$@ $<

clean:
	latexmk -C
	/bin/rm -rf $(GENPDFS) _minted* *-SAVE-ERROR $(PDFS)

proof:
	echo "weasel words: "
	sh bin/noweasel *.tex
	echo
	echo "passive voice: "
	sh bin/nopassive *.tex
	echo
	echo "duplicates: "
	perl bin/nodups *.tex
