#!python3

"""
Load the author database from the support directory and
read the builders database, and list builders who are
possibly missing.

  python3 support/missing-builders.py

This program requires the "yaml" package to be installed.

"""
from __future__ import print_function
import os
import sys
import os.path
import re
import yaml

# This file currently a copy and paste from the static builders
# HTML web page, tab-separated columns
BUILDERS_FILE = "builders.txt"


def cleanSurname(surname):
    for c in "'{} \\":
        surname = surname.replace(c, "")
    return surname


# Paper author database
infile = os.path.join("support", "authordb.yaml")

with open(infile, "r") as fh:
    authordb = yaml.safe_load(fh)

# list of authors. Each element is a dict with keys
# name: Surname
# initials: A.B.
# orcid: ORCID (can be None)
# affil: List of affiliation labels
# altaffil: List of alternate affiliation text
authorList = authordb["authors"]

authors = {}
for auth in authorList:
    # For spaces in surnames use a ~
    surname = cleanSurname(auth["name"])
    author = (auth["initials"], auth["name"], auth["affil"])
    if surname in authors:
        authors[surname].append(author)
    else:
        authors[surname] = [author]

# Now get builder list
builders = {}
with open(BUILDERS_FILE, "r") as fh:
    for row in fh:
        row = row.strip()
        builder = row.split("\t")
        surname = builder[1]
        surname = cleanSurname(surname)
        if surname in builders:
            builders[surname].append(builder)
        else:
            builders[surname] = [builder]

# Now go through builders and see if they are in authors
for builderSurname in builders:
    if builderSurname not in authors:
        text = str(builders[builderSurname])
        text = text.replace("[", "")
        text = text.replace("]", "")
        print("Missing builder: {}".format(text))
        continue
