'''
    Script:      xjtools.py
    Description: ...
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        1st October 2020
'''

import argparse
import sys
from lib import xjtoolslib
from lib import xjinstaller

_VERSION = "2.0.0"
_PROTECTED_TOOL_NAMES = ["new", "edit", "delete", "duplicate", "list", "rename", "install"]

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='xj-tools.py (v{0})'.format(_VERSION), formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("command", help='The command that you want to run\r\n' +
                                    '* list\r\n' +
                                    '* new TOOL_NAME\r\n' +
                                    '* edit TOOL_NAME\r\n' +
                                    '* rename TOOL_NAME NEW_TOOL_NAME\r\n' +
                                    '* duplicate TOOL_NAME NEW_TOOL_NAME\r\n' +
                                    '* delete TOOL_NAME ')
    p.add_argument("tool_name", nargs='?', help='The name of the tool, if required')
    p.add_argument('new_tool_name', nargs='?', help='The name of new tool, if required')
    p.add_argument('-v', '--verbose', help='Enable verbose output', action='store_true')
    args = p.parse_args()

    try:
        if (args.command == "install"):
            print("Install TBD")
            # Needs to add to .zshrc/.bashrc
            # Needs to install requirements
            # python3 -m pip install -r requirements.txt
        elif (args.command == "list"): 
            xjtoolslib._list_scripts()
        elif (args.command == "new"):
            xjtoolslib._new_tool(args.tool_name)
        elif (args.command == "edit"):
            xjtoolslib._edit_tool(args.tool_name)
        elif (args.command == "rename"):
            xjtoolslib._rename_tool(args.tool_name, args.new_tool_name)
        elif (args.command == "duplicate"):
            xjtoolslib._duplicate_tool(args.tool_name, args.new_tool_name)
        elif (args.command == "delete"):
            xjtoolslib._delete_tool(args.tool_name)
        else:
            print("Unrecognised command")
    except Exception as e:
        print("[xjtools] Error: {0}".format(str(e)))