import unicodedata
import re


def strip_accents(s):
    return "".join(
        c
        for c in unicodedata.normalize("NFD", str(s))
        if unicodedata.category(c) != "Mn"
    )


def sluggify(s, sep="_"):
    pattern = re.compile(r"[-_\W]+")
    return pattern.sub(sep, strip_accents(s).lower()).strip(sep)
