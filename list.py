'''
    Script:      my-tools/list.py
    Description: List all of the scripts in this directory
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        06 May 2020
'''

import argparse
import os
import sys
import re
import prettytable

_VERSION = "1.0.1"

def _list_scripts():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir(root_dir)
    re_version = "_VERSION = \"(.*)\""
    re_desc = "    Description: (.*)"

    table = prettytable.PrettyTable(["Tool", "Version", "Description"])
    table.align = "l"
    table.align["Version"] = "c"

    for index, file in enumerate(files):
        if file[-3:] == ".py":
            version = None
            desc = None
            with open(os.path.join(root_dir, file), 'r') as f:
                for index, line in enumerate(f):
                    re_find_version = re.match(re_version, line)
                    re_find_desc = re.match(re_desc, line)
                    if re_find_version:
                        version = re_find_version.groups()[0]
                    elif re_find_desc:
                        desc = re_find_desc.groups()[0]
                    if version and desc:
                        break
            table.add_row([file.replace(".py",""), version, desc])
    print(table)

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='my-tools/list.py (v{0})'.format(_VERSION))
    # p.add_argument("positional_argument")
    # p.add_argument('-s', '--string', help='')
    # p.add_argument('-b', '--bool', help='', action='store_true')
    args = p.parse_args()

    _list_scripts()
