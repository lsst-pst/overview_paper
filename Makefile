#
#


TEX=$(*.tex)

all: $(TEX)
	latexmk  -bibtex -pdf -f lsst.tex

clean :
	latexmk -c
	rm lsst.pdf
