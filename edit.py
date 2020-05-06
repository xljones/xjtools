'''
    Script:  my-tools/edit.py
    Author:  Xander Jones (xander@xljones.com)
    Web:     xljones.com
    Date:    06 May 2020
'''
        
import argparse
import os
import sys

_VERSION = "1.0.0"

def _edit_tool(name):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(name)
    filepath = os.path.join(root_dir, filename)
    
    if not os.path.exists(filepath):
        print("Error: File '{0}' does not exist. Create it with: tools new {1}".format(filename, name))
        exit(1)
    else:
        print("Openning '{0}' in Atom".format(filepath))
        os.system("atom {0}".format(filepath))

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='my-tools/edit.py (v{0})'.format(_VERSION))
    p.add_argument("tool_name")
    # p.add_argument('-s', '--string', help='')
    # p.add_argument('-b', '--bool', help='', action='store_true')
    args = p.parse_args()
        
    _edit_tool(args.tool_name)
