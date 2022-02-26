'''
    Script:      xjtools.py
    Description: ...
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        1st October 2020
'''

import argparse
import xjtools.core
import xjtools.const

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description=f"xjtools (v{xjtools.const.VERSION})",
        formatter_class=argparse.RawTextHelpFormatter
    )
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
        if args.command == "list":
            xjtools.core.list_tools()
        elif args.command == "new":
            xjtools.core.new_tool(args.tool_name)
        elif args.command == "edit":
            xjtools.core.edit_tool(args.tool_name)
        elif args.command == "rename":
            xjtools.core.rename_tool(args.tool_name, args.new_tool_name)
        elif args.command == "duplicate":
            xjtools.core.duplicate_tool(args.tool_name, args.new_tool_name)
        elif args.command == "delete":
            xjtools.core.delete_tool(args.tool_name)
        else:
            xjtools.core.output_msg("Unrecognised command")
    except Exception as e:
        xjtools.core.output_msg(f"Error: {str(e)}")
