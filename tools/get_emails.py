"""
    Script:      tools/get_emails.py
    Description: Extracts email addresses from a given raw text file
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        01 Feb 2021
"""

import argparse
import os
import re

_VERSION = "1.0.0"


def _extract_emails(input_file):
    print("Extracting email addresses from '{0}'".format(input_file))
    file = open(input_file, "r").read()
    match = re.findall(r"[\w\.-]+@[\w\.-]+", file)
    dedupe = list(set(match))
    for index, email in enumerate(dedupe):
        print("[{0}] {1}".format(index + 1, email))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="tools/get_emails.py (v{0})".format(_VERSION))
    p.add_argument("input_filepath", help="the raw input file with email addresses to extract")
    args = p.parse_args()

    _extract_emails(os.path.abspath(args.input_filepath))
