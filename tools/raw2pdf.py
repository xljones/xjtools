"""
    Script:      tools/raw2pdf.py
    Description: Convert a raw string into a pdf
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        04 Dec 2023
"""

import argparse
import os
import sys
from typing import Optional

_VERSION = "1.0.0"


def raw2pdf(raw_data: str, output_filename: Optional[str]) -> None:
    print("Hello World! from {0}".format(__file__))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="tools/raw2pdf.py (v{0})".format(_VERSION))
    p.add_argument("raw_data")
    p.add_argument("-o", "--output", help="The file name to output to e.g. test.pdf")
    args = p.parse_args()

    raw2pdf(args.raw_data, args.output)
