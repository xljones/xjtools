"""
    Script:      lib/xjtoolslib.py
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
"""

import argparse
import datetime
import os
import re
import shutil
import sys

import prettytable

from . import xjconst

"""
Description: List all of the scripts in the
             _TOOLS_DIR directory
"""


def _list_tools():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.abspath(os.path.join(root_dir, xjconst._TOOLS_DIR))
    files = os.listdir(filepath)
    re_version = '_VERSION = "(.*)"'
    re_desc = "    Description: (.*)"

    table = prettytable.PrettyTable(["#", "Tool", "Version", "Description"])
    table.align = "l"

    for index, file in enumerate(files):
        if file[-3:] == ".py":
            version = None
            desc = None
            with open(os.path.join(root_dir, xjconst._TOOLS_DIR, file), "r") as f:
                for line in f:
                    re_find_version = re.match(re_version, line)
                    re_find_desc = re.match(re_desc, line)
                    if re_find_version:
                        version = re_find_version.groups()[0]
                    elif re_find_desc:
                        desc = re_find_desc.groups()[0]
                    if version and desc:
                        break
            table.add_row([index, file.replace(".py", ""), version, desc])
    _output_msg("Listing tools found in {0}".format(filepath))
    print(table)


"""
Description: Create a new tool in the tools directory
"""


def _new_tool(tool_name):
    # Check a tool name has been given
    if tool_name == None:
        raise AttributeError("No new tool name given to create")

    # Check the tool name is not protected
    if tool_name in xjconst._PROTECTED_TOOL_NAMES:
        raise ValueError(
            "'{0}' is a protected tool name, try using another name".format(tool_name)
        )

    # Check the tool does not already exist
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filepath = os.path.abspath(os.path.join(root_dir, xjconst._TOOLS_DIR, filename))
    if os.path.exists(filepath):
        raise FileExistsError("Tool named '{0}' already exists".format(tool_name))

    # Create the tool if no errors raised
    else:
        f = open(filepath, "w+")
        newfile = xjconst._NEWFILE
        for find, replace in {
            "$FILENAME": filename,
            "$DATE": datetime.datetime.now().strftime(xjconst._DATETIME_FORMAT),
        }.items():
            newfile = newfile.replace(find, replace)
        f.write(newfile)
        f.close()
        _output_msg(
            "Done: A new tool '{0}' has been created. Use `tools edit {0}` to edit".format(
                tool_name
            )
        )


"""
Description: Edit a tool in this directory
"""


def _edit_tool(tool_name):
    # Check a tool name has been given
    if tool_name == None:
        raise AttributeError("No new tool name given to edit")

    # Check the tool exists
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filepath = os.path.abspath(os.path.join(root_dir, xjconst._TOOLS_DIR, filename))
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            "'{0}' does not exist. Create it with: `tools new {1}`".format(
                filename, tool_name
            )
        )

    # Edit the tool if no errors raised
    else:
        _output_msg("Openning '{0}' with `{1}`".format(filepath, xjconst._EDIT_TOOL))
        os.system("{0} {1}".format(xjconst._EDIT_TOOL, filepath))


"""
Description: Takes in an old tool, and gives it a new name
             It will also update the scriptname, date inside
             the file, and argparser name.
"""


def _rename_tool(tool_name, new_tool_name):
    # Check old tool name param has been given
    if tool_name == None:
        raise AttributeError("Tool name was not given to rename")
    # Check new tool name to rename to has been given
    elif new_tool_name == None:
        raise AttributeError("New tool name was not given to rename to")
    # Check the tool name is not protected
    if new_tool_name in xjconst._PROTECTED_TOOL_NAMES:
        raise ValueError(
            "'{0}' is a protected tool name, try using another name".format(
                new_tool_name
            )
        )

    # Check file exists, and new rename name is not already taken
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filename_new = "{0}.py".format(new_tool_name)
    filepath = os.path.abspath(os.path.join(root_dir, xjconst._TOOLS_DIR, filename))
    filepath_new = os.path.abspath(
        os.path.join(root_dir, xjconst._TOOLS_DIR, filename_new)
    )

    re_scriptname = r"^(    Script:      tools\/)(.*)(\.py)"
    re_date = r"^(    Date:        )(\w+ \w+ \w+)"
    re_argparser = r"^(    p = argparse\.ArgumentParser\(description=\'tools\/)(.*)(\.py \(v\{0\}\)\'\.format\(_VERSION\)\))"

    if not os.path.exists(filepath):
        raise FileNotFoundError("Tool '{0}' does not exist".format(tool_name))
    elif os.path.exists(filepath_new):
        raise FileExistsError(
            "There is already a tool called '{0}', choose another new name".format(
                new_tool_name
            )
        )

    # if no errors raised, rename the tool
    else:
        confirmation = input(
            "{0} Are you sure you want to rename '{1}' to '{2}'? [Y/n]: ".format(
                xjconst._PRINT_PREFIX, tool_name, new_tool_name
            )
        )
        if confirmation.lower() == "y":
            with open(filepath_new, "w") as newf:
                with open(filepath, "r") as f:
                    for index, line in enumerate(f):
                        newline = None
                        re_find_scriptname = re.match(re_scriptname, line)
                        re_find_date = re.match(re_date, line)
                        re_find_argparser = re.match(re_argparser, line)
                        if re_find_scriptname:
                            newline = "{0}{1}{2}\r\n".format(
                                re_find_scriptname.groups()[0],
                                new_tool_name,
                                re_find_scriptname.groups()[2],
                            )
                            _output_msg(
                                ">> Found scriptname on line {0}, replace with:".format(
                                    index + 1
                                )
                            )
                            _output_msg("'{0}'".format(newline.rstrip()))
                        elif re_find_date:
                            newdate = datetime.datetime.now().strftime(
                                xjconst._DATETIME_FORMAT
                            )
                            newline = "{0}{1}\r\n".format(
                                re_find_date.groups()[0], newdate
                            )
                            _output_msg(
                                ">> Found date on line {0}, replace with:".format(
                                    index + 1
                                )
                            )
                            _output_msg("'{0}'".format(newline.rstrip()))
                        elif re_find_argparser:
                            newline = "{0}{1}{2}\r\n".format(
                                re_find_argparser.groups()[0],
                                new_tool_name,
                                re_find_argparser.groups()[2],
                            )
                            _output_msg(
                                ">> Found argparser on line {0}, replace with:".format(
                                    index + 1
                                )
                            )
                            _output_msg("'{0}'".format(newline.rstrip()))
                        else:
                            newline = line
                        newf.write(newline)
            os.remove(filepath)


"""
Description: Copy a tool and rename the internals
"""


def _duplicate_tool(tool_name, new_tool_name):
    # Check old tool name param has been given
    if tool_name == None:
        raise AttributeError("Tool name was not given to duplicate")
    # Check new tool name to duplicate to has been given
    elif new_tool_name == None:
        raise AttributeError("New tool name was not given to name duplicate")
    # Check the tool name is not protected
    if new_tool_name in xjconst._PROTECTED_TOOL_NAMES:
        raise ValueError(
            "'{0}' is a protected tool name, try using another name".format(
                new_tool_name
            )
        )

    # Check file exists, and new duplicate name is not already taken
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filename_new = "{0}.py".format(new_tool_name)
    filepath = os.path.abspath(os.path.join(root_dir, xjconst._TOOLS_DIR, filename))
    filepath_new = os.path.abspath(
        os.path.join(root_dir, xjconst._TOOLS_DIR, filename_new)
    )

    re_scriptname = r"^(    Script:      tools\/)(.*)(\.py)"
    re_date = r"^(    Date:        )(\w+ \w+ \w+)"
    re_argparser = r"^(    p = argparse\.ArgumentParser\(description=\'tools\/)(.*)(\.py \(v\{0\}\)\'\.format\(_VERSION\)\))"

    if not os.path.exists(filepath):
        raise FileNotFoundError("Tool '{0}' does not exist".format(tool_name))
    elif os.path.exists(filepath_new):
        raise FileExistsError(
            "There is already a tool called '{0}', choose another new name".format(
                new_tool_name
            )
        )

    # If no errors raised, duplicate the tool
    else:
        with open(filepath_new, "w") as newf:
            with open(filepath, "r") as f:
                for index, line in enumerate(f):
                    newline = None
                    re_find_scriptname = re.match(re_scriptname, line)
                    re_find_date = re.match(re_date, line)
                    re_find_argparser = re.match(re_argparser, line)
                    if re_find_scriptname:
                        newline = "{0}{1}{2}\r\n".format(
                            re_find_scriptname.groups()[0],
                            new_tool_name,
                            re_find_scriptname.groups()[2],
                        )
                        _output_msg(
                            ">> Found scriptname on line {0}, replace with:".format(
                                index + 1
                            )
                        )
                        _output_msg("'{0}'".format(newline.rstrip()))
                    elif re_find_date:
                        newdate = datetime.datetime.now().strftime(
                            xjconst._DATETIME_FORMAT
                        )
                        newline = "{0}{1}\r\n".format(re_find_date.groups()[0], newdate)
                        _output_msg(
                            ">> Found date on line {0}, replace with:".format(index + 1)
                        )
                        _output_msg("'{0}'".format(newline.rstrip()))
                    elif re_find_argparser:
                        newline = "{0}{1}{2}\r\n".format(
                            re_find_argparser.groups()[0],
                            new_tool_name,
                            re_find_argparser.groups()[2],
                        )
                        _output_msg(
                            ">> Found argparser on line {0}, replace with:".format(
                                index + 1
                            )
                        )
                        _output_msg("'{0}'".format(newline.rstrip()))
                    else:
                        newline = line
                    newf.write(newline)


"""
Description: Deletes the selected tool from the ../tools/ dir
             by moving it into a subfolder ../tools/.deleted
"""


def _delete_tool(tool_name):
    # Check tool name param has been given
    if tool_name == None:
        raise AttributeError("Tool name was not given to delete")

    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filepath = os.path.abspath(os.path.join(root_dir, xjconst._TOOLS_DIR, filename))

    if not os.path.exists(filepath):
        raise FileNotFoundError("Tool '{0}' does not exist".format(tool_name))
    else:
        confirmation = input(
            "{0} Are you sure you want to delete '{1}'? [Y/n]: ".format(
                xjconst._PRINT_PREFIX, tool_name
            )
        )
        if confirmation.lower() == "y":
            deleted_dir = os.path.join(root_dir, xjconst._TOOLS_DIR, ".deleted")
            if not os.path.exists(deleted_dir):
                os.mkdir(deleted_dir)

            deleted_filepath = os.path.abspath(os.path.join(deleted_dir, filename))
            deleted_file_index = 0
            while os.path.exists(
                "{0}_{1}".format(deleted_filepath, deleted_file_index)
            ):
                deleted_file_index += 1

            shutil.move(
                filepath, "{0}_{1}".format(deleted_filepath, deleted_file_index)
            )
            _output_msg(
                "Done: Tool '{0}' has been moved to the '.deleted' directory".format(
                    tool_name
                )
            )


"""
Description: Manages output messages from the library
"""


def _output_msg(msg):
    print("{0} {1}".format(xjconst._PRINT_PREFIX, msg))


if __name__ == "__main__":
    _output_msg(
        "Error: xjtoolslib.py is a library, and can't be called directly. Try using `cd .. && python3 xjtools.py -h` for help"
    )
