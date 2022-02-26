'''
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
'''

# Command to run to edit a file
# e.g. if you use Atom: `atom`
#      if using vscode: `code`
EDIT_TOOL = "code"

# The location of the tools directory relative
# to the location of this script.
TOOLS_DIR = "../tools"

# The format for the datetime stamp whenver
# it is written to a tool file
DATETIME_FORMAT = "%d %b %Y"

# The new file prototype that will be used to
# create all new scripts from.
NEWFILE = """'''
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
    p = argparse.ArgumentParser(description=f"tools/$FILENAME (v{_VERSION})")
    # p.add_argument("positional_argument")
    # p.add_argument("-s", "--string", help="")
    # p.add_argument("-b", "--bool", help="", action="store_true")
    args = p.parse_args()

    _do_something()"""

# The prefix before printing any lines
PRINT_PREFIX = "[xjtools]"

# A list of tool names that cannot be used
# These are used by the library itself.
PROTECTED_TOOL_NAMES = ["new", "edit", "delete", "duplicate", "list", "rename", "help"]

# a dictionary of regexes used to parse tool files
REGEXES = {
    "version":     r"_VERSION = \"(.*)\"",
    "description": r"    Description: (.*)",
    "scriptname":  r"^(    Script:      tools\/)(.*)(\.py)",
    "date":        r"^(    Date:        )(\w+ \w+ \w+)",
    "argparser":   r"^(    p = argparse\.ArgumentParser\(description=\"tools\/)(.*)(\.py \(v\{_VERSION\}\)\"\))"
}

if __name__ == "__main__":
    raise RuntimeError("Error: this is the constants file, and can't be called directly. ")
