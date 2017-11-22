#
#

SRC=$(lsst.tex)

OBJ=$(SRC:.tex=.pdf)

all: $(tex)
	latexmk -bibtex -pdf -f $(SRC)

clean :
	latexmk -c
	rm lsst.pdf

