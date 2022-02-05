'''
    Script:      tools/get_emails.py
    Description: Extracts email addresses from a given raw text file
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        01 Feb 2021
'''

import argparse
import re
import os

_VERSION = "1.0.0"

def _extract_emails(input_file):
    print("Extracting email addresses from '{input_file}'")
    with open(input_file, "r").read() as file:
        match = re.findall(r'[\w\.-]+@[\w\.-]+', file)
        dedupe = list(set(match))
        for index, email in enumerate(dedupe):
            print("[{index+1}] {email}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description='tools/get_emails.py (v{_VERSION})')
    p.add_argument("input_filepath", help="the raw input file with email addresses to extract")
    args = p.parse_args()

    _extract_emails(os.path.abspath(args.input_filepath))
