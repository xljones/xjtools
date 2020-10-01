'''
    Script:      my-tools:new.py
    Description: Create a new tool in this directory
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        06 May 2020
'''

import datetime
import argparse
import os
import sys

_VERSION = "1.0.2"

_NEWFILE = """'''
    Script:      my-tools:$FILENAME
    Description: ...
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        $DATE
'''

import argparse
import os
import sys

_VERSION = \"1.0.0\"

def _do_something():
    print("Hello World! from {0}".format(__file__))

if (__name__ == \"__main__\"):
    p = argparse.ArgumentParser(description='my-tools:$FILENAME (v{0})'.format(_VERSION))
    # p.add_argument("positional_argument")
    # p.add_argument('-s', '--string', help='')
    # p.add_argument('-b', '--bool', help='', action='store_true')
    args = p.parse_args()

    _do_something()"""

def _create_new_tool(newfile, tool_name):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filepath = os.path.join(root_dir, "tools", filename)

    if os.path.exists(filepath):
        print("Error: Tool '{0}' already exists".format(tool_name))
        exit(1)
    else:
        f = open(filepath, "w+")
        for find, replace in {"$FILENAME":filename, "$NAME":tool_name, "$DATE":datetime.datetime.now().strftime("%d %b %Y")}.items():
            newfile = newfile.replace(find, replace)
        f.write(newfile)
        f.close()
        print("Done: A new tool '{0}' has been created. Use `tools edit {0}` to edit".format(tool_name))

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='my-tools/new.py (v{0})'.format(_VERSION))
    p.add_argument("tool_name")
    # p.add_argument('-l', '--long', help='')
    # p.add_argument('-l', '--long', help='', action='store_true')
    args = p.parse_args()

    _create_new_tool(_NEWFILE, args.tool_name)
