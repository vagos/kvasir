## This is the Makefile for the template paper. All you need to do is 
## edit "TARGETS" below to the name of the main .tex file for your paper.

TARGETS = draft

TEXFILES = $(wildcard *.tex)
FIGURES =$(wildcard figures/*.pdf figures/*.tex)
GENPDFS = $(patsubst %.svg,%.pdf,$(wildcard figures/*.svg))
PDFS = $(addsuffix .pdf,$(TARGETS))
BIBFILES=bib.bib

LATEXMK      = latexmk
LATEXMKFLAGS = -pdf \
               -pdflatex="xelatex --shell-escape -interaction=nonstopmode" \
               -use-make

all: $(PDFS)

%.pdf: $(TEXFILES) $(FIGURES) $(BIBFILES)
	$(LATEXMK) $(LATEXMKFLAGS) $<

%.pdf: %.svg
	inkscape --export-pdf=$@ $<

continuous: draft.tex
	$(LATEXMK) -pdf \
	-pdflatex="xelatex --shell-escape -interaction=nonstopmode" \
	-pvc $<

once:
	pdflatex --shell-escape draft.tex
	bibtex draft
	pdflatex --shell-escape draft.tex
	pdflatex --shell-escape draft.tex

%.blg: $(GENPDFS) $(BIBFILES)
	pdflatex --shell-escape $*.tex
	bibtex $*
	pdflatex --shell-escape $*.tex

%.toc: %.tex $(GENPDFS)
	pdflatex --shell-escape $*.tex

clean:
	/bin/rm -rf $(PDFS) *.out *.fdb_latexmk *.synctex.gz *.dvi *.aux *.ps *~ *.log *.lot *.lof *.toc *.blg *.bbl -r _minted* $(GENPDFS)

# Check style:
proof:
	echo "weasel words: "
	sh bin/noweasel *.tex
	echo
	echo "passive voice: "
	sh bin/nopassive *.tex
	echo
	echo "duplicates: "
	perl bin/nodups *.tex


FORCE:
