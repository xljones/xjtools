'''
    Script:      my-tools:duplicate.py
    Description: ...
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        07 May 2020
'''

import argparse
import os
import sys

_VERSION = "1.0.0"

def _do_something():
    print("Hello World! from {0}".format(__file__))

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='my-tools:duplicate.py (v{0})'.format(_VERSION))
    # p.add_argument("positional_argument")
    # p.add_argument('-s', '--string', help='')
    # p.add_argument('-b', '--bool', help='', action='store_true')
    args = p.parse_args()

    _do_something()
