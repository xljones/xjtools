'''
    Script:      lib/list.py
    Description: List all of the scripts in the
                 ../tools directory
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
'''

import argparse
import os
import sys
import re
import prettytable

def _list_scripts(tools_directory = "../tools"):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir(os.path.join(root_dir, tools_directory))
    re_version = "_VERSION = \"(.*)\""
    re_desc = "    Description: (.*)"

    table = prettytable.PrettyTable(["#", "Tool", "Version", "Description"])
    table.align = "l"

    for index, file in enumerate(files):
        if file[-3:] == ".py":
            version = None
            desc = None
            with open(os.path.join(root_dir, tools_directory, file), 'r') as f:
                for line in f:
                    re_find_version = re.match(re_version, line)
                    re_find_desc = re.match(re_desc, line)
                    if re_find_version:
                        version = re_find_version.groups()[0]
                    elif re_find_desc:
                        desc = re_find_desc.groups()[0]
                    if version and desc:
                        break
            table.add_row([index, file.replace(".py",""), version, desc])
    print(table)

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='lib/list.py')
    args = p.parse_args()

    _list_scripts()
