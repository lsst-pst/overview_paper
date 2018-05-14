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
import os.path
import yaml

# This file currently a copy and paste from the static builders
# HTML web page, tab-separated columns
BUILDERS_FILE = "builders.txt"


def deriveNameKey(surname, initials):
    """Build key for indexing authors.
    """
    # Clean surname of latex
    for c in "'{} \\":
        surname = surname.replace(c, "")
        if initials is not None:
            initials = initials.replace(c, "")

    if initials is None:
        initials = ""
    else:
        initials = initials[0]

    return "{}{}".format(surname, initials)


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
authors_by_surname = {}
for auth in authorList:
    # For spaces in surnames use a ~
    nameKey = deriveNameKey(auth["name"], auth["initials"])
    author = (auth["initials"], auth["name"], auth["affil"])
    if nameKey in authors:
        authors[nameKey].append(author)
    else:
        authors[nameKey] = [author]
    nameKey = deriveNameKey(auth["name"], None)
    if nameKey in authors_by_surname:
        authors_by_surname[nameKey].append(author)
    else:
        authors_by_surname[nameKey] = [author]

# Now get builder list
builders = {}
builders_by_surname = {}
with open(BUILDERS_FILE, "r") as fh:
    for row in fh:
        row = row.strip()
        builder = row.split("\t")
        nameKey = deriveNameKey(builder[1], builder[0])
        surnameKey = deriveNameKey(builder[1], None)
        if nameKey in builders:
            builders[nameKey].append(builder)
        else:
            builders[nameKey] = [builder]
        builders_by_surname[nameKey] = surnameKey

# Now go through builders and see if they are in authors
for builderKey in builders:
    text = str(builders[builderKey])
    text = text.replace("[", "")
    text = text.replace("]", "")

    # If the surname does not exist in authors then it is clearly missing
    if builderKey not in authors:
        print("Missing builder: {}".format(text))
        # Some people have different initials on the builder list.
        # "William -> Bill" etc
        surname = builders_by_surname[builderKey]
        if surname in authors_by_surname:
            print("-> Possibly present as {}".format(authors_by_surname[surname]))
        continue

    # Two builders with same surname and first initial
    if len(builders[builderKey]) > 1:
        print("Two builders but one author. Check: {}".format(text))
        print("-> Author list: {}".format(authors[builderKey]))
