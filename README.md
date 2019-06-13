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
The list of authors is defined in `authors.yaml` in the root directory.
This file contains a list of author IDs in the order in which they appear in this paper.
The author IDs must match those found in the `lsst-texmf/etc/authordb.yaml` file.
If a new author is added to the paper, a corresponding entry must be created in [lsst-texmf](https://github.com/lsst/lsst-texmf).
A new authors tex file can then be created by running:
```
% python3 lsst-texmf/bin/db2authors.py > authors.tex
```
If a submodule is used then remember to update the `lsst-texmf` submodule with the newest version of the database.
The `yaml` python module must be installed.

Please send questions and comments to Zeljko Ivezic (ivezic@astro.washington.edu)
