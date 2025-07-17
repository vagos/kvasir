## This is the Makefile for the template paper.
## Set TARGETS to the name of your main .tex file (without extension)

TARGETS = draft

TEXFILES = $(wildcard *.tex)
FIGURES = $(wildcard figures/*.pdf figures/*.tex)
SVGFILES = $(wildcard figures/*.svg)
GENPDFS = $(patsubst %.svg,%.pdf,$(SVGFILES))
BIBFILES = $(wildcard *.bib)
PDFS = $(addsuffix .pdf,$(TARGETS))

LATEXMK = latexmk
LATEXMK_OPTS = -lualatex -shell-escape

all: $(PDFS)

$(PDFS): %.pdf: %.tex $(TEXFILES) $(FIGURES) $(GENPDFS) $(BIBFILES)
	$(LATEXMK) $(LATEXMK_OPTS) $*

%.pdf: %.svg
	inkscape --export-filename=$@ $<

once:
	$(LATEXMK) $(LATEXMK_OPTS) -gg $(TARGETS)

clean:
	$(LATEXMK) -C
	/bin/rm -f $(GENPDFS)

proof:
	echo "weasel words:"
	sh bin/noweasel *.tex
	echo
	echo "passive voice:"
	sh bin/nopassive *.tex
	echo
	echo "duplicates:"
	perl bin/nodups *.tex
