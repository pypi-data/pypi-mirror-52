#!/usr/bin/env python3

"""Convert a docx file to json."""

import argparse
import json
import sys

import parsoc

PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument("file", help="path of the docx file")


def main(args=None):
    """Entry point of the script."""
    opts = PARSER.parse_args(args)
    doc = parsoc.Document(opts.file)
    struct = parsoc.parse_document(doc)

    json.dump(struct, sys.stdout)


if __name__ == "__main__":
    main()
