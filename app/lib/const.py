"""
    Script:      lib/xjconst.py
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
"""

from app.lib import helpers

# Command to run to edit a file
# e.g. if you use Atom: `atom`
#      if using vscode: `code -add`
_EDIT_TOOL = "code -add"

# The location of the tools directory relative
# to the location of this script.
_TOOLS_DIR = "../../tools"

# The format for the datetime stamp whenver
# it is written to a tool file
_DATETIME_FORMAT = "%d %b %Y"

# The new file prototype that will be used to
# create all new scripts from.
_NEWFILE = """'''
    Script:      tools/$FILENAME
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
    p = argparse.ArgumentParser(description='tools/$FILENAME (v{0})'.format(_VERSION))
    # p.add_argument("positional_argument")
    # p.add_argument('-s', '--string', help='')
    # p.add_argument('-b', '--bool', help='', action='store_true')
    args = p.parse_args()

    _do_something()"""

# The prefix before printing any lines
_PRINT_PREFIX = "[xjtools]"

# A list of tool names that cannot be used
# These are used by the library itself.
_PROTECTED_TOOL_NAMES = ["new", "edit", "delete", "duplicate", "list", "rename", "help"]

if __name__ == "__main__":
    helpers._output_msg(
        "Error: xjconst.py is a library, and can't be called directly. Try using `cd .. && python3 xjtools.py -h` for help"
    )
