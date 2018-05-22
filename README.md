LSST overview paper, available as
<http://arxiv.org/abs/0805.2366>

Master branch gives the latest version (the same as posted to arXiv)

References are done using bibtex.

To compile and make `lsst.pdf`:
```
% make
```
or
```
% latexmk -bibtex -pdf lsst
```
or
```
% pdflatex lsst
% bibtex lsst
% pdflatex lsst
% pdflatex lsst
```

The author list is generated from a YAML database file.
Please make changes to authors by editing `support/authordb.yaml` and then running:
```
% python support/db2authors.py > authors.tex
```
This can use Python 2 or Python 3, but the `yaml` python module must be installed.

Please send questions and comments to Zeljko Ivezic (ivezic@astro.washington.edu)
