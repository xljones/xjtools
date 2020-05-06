'''
    Script:  my-tools/new.py
    Author:  Xander Jones (xander@xljones.com)
    Web:     xljones.com
    Date:    06 May 2020
'''

import datetime
import argparse
import os
import sys

_VERSION = "1.0.0"
_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
_NEWFILE = """'''
    Script:  my-tools/$FILENAME
    Author:  Xander Jones (xander@xljones.com)
    Web:     xljones.com
    Date:    $DATE
'''

import argparse
import os
import sys

_VERSION = \"1.0.0\"
_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if (__name__ == \"__main__\"):
    p = argparse.ArgumentParser(description='my-tools/$FILENAME (v{0})'.format(_VERSION))
    # p.add_argument("positional_argument")
    # p.add_argument('-s', '--string', help='')
    # p.add_argument('-b', '--bool', help='', action='store_true')
    args = p.parse_args()

    _do_something()"""

def _create_new_tool(newfile, name):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(name)
    filepath = os.path.join(root_dir, filename)
    
    if os.path.exists(filepath):
        print("Error: File '{0}' already exists".format(filename))
        exit(1)
    else:
        f = open(filepath, "w+")
        for find, replace in {"$FILENAME":filename, "$NAME":name, "$DATE":datetime.datetime.now().strftime("%d %b %Y")}.items():
            newfile = newfile.replace(find, replace)
        f.write(newfile)
        f.close()

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='my-tools/new.py (v{0})'.format(_VERSION))
    p.add_argument("tool_name")
    # p.add_argument('-l', '--long', help='')
    # p.add_argument('-l', '--long', help='', action='store_true')
    args = p.parse_args()

    _create_new_tool(_NEWFILE, args.tool_name)
