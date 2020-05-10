'''
    Script:      my-tools:rename.py
    Description: ...
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        07 May 2020
'''

import argparse
import os
import re
import sys
import semver
import datetime

_VERSION = "1.0.0"

def _rename_tool(tool_name, new_name):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filepath = os.path.join(root_dir, "tools", filename)

    re_scriptname = r'^(    Script:      my-tools:)(.*)(.py)'
    re_date = r'(    Date:        )(\w+ \w+ \w+)'
    re_argparser = r'^(    p = argparse\.ArgumentParser\(description=\'my-tools:)(.*)(\.py \(v\{0\}\)\'\.format\(_VERSION\)\))'

    if not os.path.exists(filepath):
        print("Error: Tool '{0}' does not exist".format(tool_name))
        exit(1)
    else:
        confirmation = input("Are you sure you want to rename '{0}' to '{1}'? [Y/n]: ".format(tool_name, new_name))
        if confirmation.lower() == "y":
            with open(filepath, 'r') as f:
                for index, line in enumerate(f):
                    re_find_scriptname = re.match(re_scriptname, line)
                    if re_find_scriptname:
                        newline = re.sub(re_scriptname, r'\1{0}\3'.format(new_name), line).strip()
                        print("Found scriptname on line {0}, replace with:".format(index))
                        print("'{0}'".format(newline))
                    re_find_date = re.match(re_date, line)
                    if re_find_date:
                        newdate = datetime.datetime.now().strftime("%d %b %Y")
                        newdate = "xyz"
                        newline = re.sub(re_date, r'\1{0}'.format(newdate), line).strip()
                        print("Found date on line {0}, replace with:".format(index))
                        print("'{0}'".format(newline))
                    re_find_argparser = re.match(re_argparser, line)
                    if re_find_argparser:
                        newline = re.sub(re_argparser, r'\1{0}\3'.format(new_name), line).strip()
                        print("Found argparser on line {0}, replace with:".format(index))
                        print("'{0}'".format(newline))

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='my-tools:rename.py (v{0})'.format(_VERSION))
    p.add_argument("tool_name", help='The name of the tool you want to rename')
    p.add_argument("new_name", help="The new name of the tool it will be changed to")
    # p.add_argument('-s', '--string', help='')
    # p.add_argument('-b', '--bool', help='', action='store_true')
    args = p.parse_args()

    _rename_tool(args.tool_name, args.new_name)
