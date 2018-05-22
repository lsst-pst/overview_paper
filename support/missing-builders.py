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


def deriveNameKey(surname, first, builder=False):
    """Build key for indexing authors.

    If this is a builder name then we can make corrections for
    Bill -> William and Margaret Gelman -> Johnson
    """
    # Clean surname of latex
    surname = surname.replace(r"\v", "")  # Zeljko
    if first is not None:
        first = first.replace(r"\v", "")

    for c in "'{} \\":
        surname = surname.replace(c, "")
        if first is not None:
            first = first.replace(c, "")

    if first is None:
        initial = ""
    else:
        initial = first[0]

    key = "{}{}".format(surname, initial)

    if builder:
        # Map derived key to author key, assuming different first name
        mapping = {"GelmanM": ("Margaret", "JohnsonM"),
                   "WahlB": ("Bill", "WahlW"),
                   "TysonT": ("Tony", "TysonJ"),
                   "SchoeningB": ("Bill", "SchoeningW"),
                   "KrughoffS": ("Simon", "KrughoffK"),
                   "GresslerB": ("Bill", "GresslerW"),
                   "GilmoreK": ("Kirk", "GilmoreD"),
                   "GlickB": ("Bill", "GlickW"),
                   "JuramyC": ("Claire", "Juramy-GillesC"),
                   "JonesL": ("Lynne", "JonesR"),
                   "JohnsonT": ("Tony", "JohnsonA"),
                   "Wood-VaseyM": ("Michael", "Wood-VaseyW")}
        if key in mapping:
            root, new = mapping[key]
            if first.startswith(root):
                key = new

    return key


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
        nameKey = deriveNameKey(builder[1], builder[0], builder=True)
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
