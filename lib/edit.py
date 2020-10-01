'''
    Script:      lib/edit.py
    Description: Edit a tool in this directory
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
'''

import argparse
import os
import sys

def _edit_tool(name):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(name)
    filepath = os.path.join(root_dir, "tools", filename)

    if not os.path.exists(filepath):
        print("Error: File '{0}' does not exist. Create it with: tools new {1}".format(filename, name))
        exit(1)
    else:
        print("Openning '{0}' in Atom".format(filepath))
        os.system("atom {0}".format(filepath))

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='lib/edit.py')
    p.add_argument("tool_name")
    args = p.parse_args()

    _edit_tool(args.tool_name)
