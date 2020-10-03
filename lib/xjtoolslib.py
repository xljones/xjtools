'''
    Script:      lib/xjtoolslib.py
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
'''

import argparse
import os
import sys
import re
import prettytable
import datetime
import shutil

# The location of the tools directory relative
# to the location of this script.
_TOOLS_DIR = "../tools"

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

'''
Description: List all of the scripts in the
             _TOOLS_DIR directory
'''
def _list_scripts():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir(os.path.join(root_dir, _TOOLS_DIR))
    re_version = "_VERSION = \"(.*)\""
    re_desc = "    Description: (.*)"

    table = prettytable.PrettyTable(["#", "Tool", "Version", "Description"])
    table.align = "l"

    for index, file in enumerate(files):
        if file[-3:] == ".py":
            version = None
            desc = None
            with open(os.path.join(root_dir, _TOOLS_DIR, file), 'r') as f:
                for line in f:
                    re_find_version = re.match(re_version, line)
                    re_find_desc = re.match(re_desc, line)
                    if re_find_version:
                        version = re_find_version.groups()[0]
                    elif re_find_desc:
                        desc = re_find_desc.groups()[0]
                    if version and desc:
                        break
            table.add_row([index, file.replace(".py",""), version, desc])
    print(table)

'''
Description: Create a new tool in the tools directory
'''
def _create_new_tool(tool_name):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filepath = os.path.join(root_dir, _TOOLS_DIR, filename)

    if os.path.exists(filepath):
        raise Exception("Tool '{0}' already exists".format(tool_name))
    else:
        print(tool_name)
        f = open(filepath, "w+")
        for find, replace in {"$FILENAME":filename, "$NAME":tool_name, "$DATE":datetime.datetime.now().strftime("%d %b %Y")}.items():
            newfile = _NEWFILE.replace(find, replace)
        f.write(newfile)
        f.close()
        print("Done: A new tool '{0}' has been created. Use `tools edit {0}` to edit".format(tool_name))

'''
Description: Edit a tool in this directory
'''
def _edit_tool(tool_name):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filepath = os.path.join(root_dir, _TOOLS_DIR, filename)

    if not os.path.exists(filepath):
        raise Exception("File '{0}' does not exist. Create it with: `tools new {1}`".format(filename, tool_name))
    else:
        print("Openning '{0}' in Atom".format(filepath))
        os.system("atom {0}".format(filepath))

'''
Description: Takes in an old tool, and gives it a new name
             It will also update the scriptname, date inside
             the file, and argparser name.
'''
def _rename_tool(tool_name, new_name):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filename_new = "{0}.py".format(new_name)
    filepath = os.path.join(root_dir, _TOOLS_DIR, filename)
    filepath_new = os.path.join(root_dir, _TOOLS_DIR, filename_new)

    re_scriptname = r'^(    Script:      tools\/)(.*)(\.py)'
    re_date =       r'^(    Date:        )(\w+ \w+ \w+)'
    re_argparser =  r'^(    p = argparse\.ArgumentParser\(description=\'tools\/)(.*)(\.py \(v\{0\}\)\'\.format\(_VERSION\)\))'

    if not os.path.exists(filepath):
        raise Exception("Tool '{0}' does not exist".format(tool_name))
    elif os.path.exists(filepath_new):
        raise Exception("There is already a tool called '{0}', choose another new name".format(new_name))
    else:
        confirmation = input("Are you sure you want to rename '{0}' to '{1}'? [Y/n]: ".format(tool_name, new_name))
        if confirmation.lower() == "y":
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
            os.remove(filepath)

'''
Description: Copy a tool and rename the internals
'''
def _duplicate_tool(tool_name, new_name):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filename_new = "{0}.py".format(new_name)
    filepath = os.path.join(root_dir, _TOOLS_DIR, filename)
    filepath_new = os.path.join(root_dir, _TOOLS_DIR, filename_new)

    re_scriptname = r'^(    Script:      tools\/)(.*)(\.py)'
    re_date =       r'^(    Date:        )(\w+ \w+ \w+)'
    re_argparser =  r'^(    p = argparse\.ArgumentParser\(description=\'tools\/)(.*)(\.py \(v\{0\}\)\'\.format\(_VERSION\)\))'

    if not os.path.exists(filepath):
        raise Exception("Tool '{0}' does not exist".format(tool_name))
    elif os.path.exists(filepath_new):
        raise Exception("There is already a tool called '{0}', choose another new name".format(new_name))
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

'''
Description: Deletes the selected tool from the ../tools/ dir
             by moving it into a subfolder ../tools/.deleted
'''
def _delete_tool(tool_name):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filepath = os.path.join(root_dir, _TOOLS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError("Error: Tool '{0}' does not exist".format(tool_name))
    else:
        confirmation = input("Are you sure you want to delete '{0}'? [Y/n]: ".format(tool_name))
        if confirmation.lower() == "y":
            deleted_dir = os.path.join(root_dir, _TOOLS_DIR, ".deleted")
            if not os.path.exists(deleted_dir):
                os.mkdir(deleted_dir)

            deleted_filepath = os.path.join(deleted_dir, filename)
            deleted_file_index = 0
            while os.path.exists("{0}_{1}".format(deleted_filepath, deleted_file_index)):
                deleted_file_index += 1

            shutil.move(filepath, "{0}_{1}".format(deleted_filepath, deleted_file_index))
            print("Done: Tool '{0}' has been moved to the '.deleted' directory".format(tool_name))

if (__name__ == "__main__"):
    raise Exception("[xjtools] Error: xjtoolslib.py is a library, and can't be called directly. Try using `cd .. && python3 xjtools.py -h`")
