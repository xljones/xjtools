'''
    Script:      my-tools:duplicate.py
    Description: Copy a tool and rename the internals
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        12 May 2020
'''

import argparse
import os
import sys
import re
import semver
import datetime

_VERSION = "1.0.0"

def _duplicate_tool(tool_name, new_name):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filename_new = "{0}.py".format(new_name)
    filepath = os.path.join(root_dir, "tools", filename)
    filepath_new = os.path.join(root_dir, "tools", filename_new)

    re_scriptname = r'^(    Script:      my-tools:)(.*)(\.py)'
    re_date =       r'^(    Date:        )(\w+ \w+ \w+)'
    re_argparser =  r'^(    p = argparse\.ArgumentParser\(description=\'my-tools:)(.*)(\.py \(v\{0\}\)\'\.format\(_VERSION\)\))'

    if not os.path.exists(filepath):
        print("Error: Tool '{0}' does not exist".format(tool_name))
        exit(1)
    elif os.path.exists(filepath_new):
        print("Error: There is already a tool called '{0}', choose another new name".format(new_name))
    else:
        with open(filepath_new, 'w') as newf:
            with open(filepath, 'r') as f:
                for index, line in enumerate(f):
                    newline = None
                    re_find_scriptname = re.match(re_scriptname, line)
                    re_find_date = re.match(re_date, line)
                    re_find_argparser = re.match(re_argparser, line)
                    if re_find_scriptname:
                        newline = "{0}{1}{2}\r\n".format(re_find_scriptname.groups()[0], new_name, re_find_scriptname.groups()[2])
                        print(">> Found scriptname on line {0}, replace with:".format(index+1))
                        print("'{0}'".format(newline))
                    elif re_find_date:
                        newdate = datetime.datetime.now().strftime("%d %b %Y")
                        newline = "{0}{1}\r\n".format(re_find_date.groups()[0], newdate)
                        print(">> Found date on line {0}, replace with:".format(index+1))
                        print("'{0}'".format(newline))
                    elif re_find_argparser:
                        newline = "{0}{1}{2}\r\n".format(re_find_argparser.groups()[0], new_name, re_find_argparser.groups()[2])
                        print(">> Found argparser on line {0}, replace with:".format(index+1))
                        print("'{0}'".format(newline))
                    else:
                        newline = line
                    newf.write(newline)

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='my-tools:duplicate.py (v{0})'.format(_VERSION))
    p.add_argument("tool_name", help='The name of the tool you want to copy')
    p.add_argument("new_name", help="The new name of the duplicate tool")
    # p.add_argument("positional_argument")
    # p.add_argument('-s', '--string', help='')
    # p.add_argument('-b', '--bool', help='', action='store_true')
    args = p.parse_args()

    _duplicate_tool(args.tool_name, args.new_name)
