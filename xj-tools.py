'''
    Script:      xj-tools.py
    Description: ...
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        1st October 2020
'''

import argparse
import os
import sys
from lib import list, new, edit, rename, duplicate, delete

_VERSION = "2.0.0"
_PROTECTED_TOOL_NAMES = ["new", "edit", "delete", "duplicate", "list", "rename"]

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

    if (args.command == "install"):
        print("Install TBC")
    elif (args.command == "list"): 
        list._list_scripts()
    elif (args.command == "new"):
        print("NEW")
        new._create_new_tool(args.tool_name)
    elif (args.command == "edit"):
        print("EDIT")
        edit._edit_tool(args.tool_name)
    elif (args.command == "rename"):
        print("RENAME")
        rename._rename_tool(args.tool_name, args.new_tool_name)
    elif (args.command == "duplicate"):
        print("DUPE")
        duplicate._duplicate_tool(args.tool_name, args.new_tool_name)
    elif (args.command == "delete"):
        print("DELETE")
        delete._delete_tool(args.tool_name)
    else:
        print("Unrecognised command")
    print(args)