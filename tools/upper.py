"""
    Script:      tools/upper.py
    Description: Convert any following arguments to upper case
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        06 May 2020
"""

import argparse
import os
import sys

_VERSION = "1.0.0"
_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    str = ""
    for index, arg in enumerate(sys.argv):
        if index > 0:
            str += "{0} ".format(arg.upper())

    print(str.upper())
