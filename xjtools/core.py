'''
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
'''

import os
import datetime
import re
import shutil
import prettytable
import xjtools.const

def list_tools():
    """List all of the scripts in the _TOOLS_DIR directory
    """
    tools_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        xjtools.const.TOOLS_DIR
    ))
    filenames = os.listdir(tools_path)

    table = prettytable.PrettyTable(["#", "Tool", "Version", "Description"])
    table.align = "l"

    for index, filename in enumerate(filenames):
        if filename[-3:] == ".py":
            (version, desc) = _get_tool_details(tools_path, filename)
            table.add_row([index, filename.replace(".py",""), version, desc])
    output_msg(f"Listing tools found in {tools_path}")
    print(table)

def _get_tool_details(tools_path: str, filename: str):
    version = None
    desc = None
    with open(os.path.join(tools_path, filename), 'r', encoding="utf-8") as file:
        for line in file:
            re_find_version = re.match(xjtools.const.REGEXES["version"], line)
            re_find_desc = re.match(xjtools.const.REGEXES["description"], line)
            if re_find_version:
                version = re_find_version.groups()[0]
            elif re_find_desc:
                desc = re_find_desc.groups()[0]
            if version and desc:
                break
    return (version, desc)


def new_tool(tool_name: str):
    """Create a new tool in the tools directory

    Args:
        tool_name (str): the name of the tool to create

    Raises:
        AttributeError: missing or invalid attribute given to function
        ValueError: if the tool name given is protected
        FileExistsError: if a tool with given name already exists
    """
    # Check a tool name has been given
    if tool_name is None:
        raise AttributeError("No new tool name given to create")

    # Check the tool name is not protected
    if tool_name in xjtools.const.PROTECTED_TOOL_NAMES:
        raise ValueError(f"'{tool_name}' is a protected tool name, try using another name")

    # Check the tool does not already exist
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = f"{tool_name}.py"
    filepath = os.path.abspath(os.path.join(root_dir, xjtools.const.TOOLS_DIR, filename))
    if os.path.exists(filepath):
        raise FileExistsError(f"Tool named '{tool_name}' already exists")

    # Else, create the tool if no errors raised
    with open(filepath, "w+", encoding="utf-8") as file:
        newfile = xjtools.const.NEWFILE
        for find, replace in {
            "$FILENAME":filename,
            "$DATE":datetime.datetime.now().strftime(xjtools.const.DATETIME_FORMAT)
        }.items():
            newfile = newfile.replace(find, replace)
        file.write(newfile)
    output_msg(f"Done: A new tool '{tool_name}' has been created. " \
        f"Use `tools edit {tool_name}` to edit")


def edit_tool(tool_name: str):
    """Edit a tool in this directory

    Args:
        tool_name (str): the tool name to edit

    Raises:
        AttributeError: missing or incorrect attribute given
        FileNotFoundError: tool to edit does not exist
    """
    # Check a tool name has been given
    if tool_name is None:
        raise AttributeError("No new tool name given to edit")

    # Check the tool exists
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = f"{tool_name}.py"
    filepath = os.path.abspath(os.path.join(root_dir, xjtools.const.TOOLS_DIR, filename))
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"'{filename}' does not exist. " \
            f"Create it with: `tools new {tool_name}`")

    # Else, edit the tool if no errors raised
    output_msg(f"Openning '{filepath}' with `{xjtools.const.EDIT_TOOL}`")
    os.system(f"{xjtools.const.EDIT_TOOL} {filepath}")


def rename_tool(tool_name: str, new_tool_name: str):
    """Takes in an old tool, and gives it a new name
       It will also update the scriptname, date inside
       the file, and argparser name.

    Args:
        tool_name (str): old tool name
        new_tool_name (str): name to rename to

    Raises:
        AttributeError: missing or invalid tool names given
        ValueError: protected tool name was used
        FileNotFoundError: original tool name was not found
        FileExistsError: failed to rename to already existing name
    """
    # Check old tool name param has been given
    if tool_name is None:
        raise AttributeError("Tool name was not given to rename")
    # Check new tool name to rename to has been given
    if new_tool_name is None:
        raise AttributeError("New tool name was not given to rename to")
    # Check the tool name is not protected
    if new_tool_name in xjtools.const.PROTECTED_TOOL_NAMES:
        raise ValueError(f"'{new_tool_name}' is a protected tool name, try using another name")

    # Check file exists, and new rename name is not already taken
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.abspath(os.path.join(
        root_dir,
        xjtools.const.TOOLS_DIR,
        f"{tool_name}.py"
    ))
    filepath_new = os.path.abspath(os.path.join(
        root_dir,
        xjtools.const.TOOLS_DIR,
        f"{new_tool_name}.py"
    ))

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Tool '{tool_name}' does not exist")
    if os.path.exists(filepath_new):
        raise FileExistsError(f"There is already a tool called '{new_tool_name}', " \
            "choose another new name")

    # if no errors raised, rename the tool
    confirmation = input(f"{xjtools.const.PRINT_PREFIX} Are you sure you want to " \
        f"rename '{tool_name}' to '{new_tool_name}'? [Y/n]: ")
    if confirmation.lower() == "y":
        with open(filepath_new, 'w', encoding="utf-8") as newf:
            with open(filepath, 'r', encoding="utf-8") as oldf:
                for index, line in enumerate(oldf):
                    newline = None
                    re_find_scriptname = re.match(xjtools.const.REGEXES["scriptname"], line)
                    re_find_date = re.match(xjtools.const.REGEXES["date"], line)
                    re_find_argparser = re.match(xjtools.const.REGEXES["argparser"], line)
                    if re_find_scriptname:
                        newline = f"{re_find_scriptname.groups()[0]}" \
                            f"{new_tool_name}" \
                            f"{re_find_scriptname.groups()[2]}\r\n"
                        output_msg(f">> Found scriptname on line {index+1}, replace with:")
                        output_msg(f"'{newline.rstrip()}'")
                    elif re_find_date:
                        newdate = datetime.datetime.now().strftime(xjtools.const.DATETIME_FORMAT)
                        newline = f"{re_find_date.groups()[0]}{newdate}\r\n"
                        output_msg(f">> Found date on line {index+1}, replace with:")
                        output_msg(f"'{newline.rstrip()}'")
                    elif re_find_argparser:
                        newline = f"{re_find_argparser.groups()[0]}" \
                            f"{new_tool_name}" \
                            f"{re_find_argparser.groups()[2]}\r\n"
                        output_msg(f">> Found argparser on line {index+1}, replace with:")
                        output_msg(f"'{newline.rstrip()}'")
                    else:
                        newline = line
                    newf.write(newline)
        os.remove(filepath)


def duplicate_tool(tool_name: str, new_tool_name: str):
    """Copy a tool and rename the internals

    Args:
        tool_name (str): _description_
        new_tool_name (str): _description_

    Raises:
        AttributeError: missing or invalid tool names given
        ValueError: protected tool name was used
        FileNotFoundError: original tool name was not found
        FileExistsError: failed to duplicate to already existing name
    """
    # Check old tool name param has been given
    if tool_name is None:
        raise AttributeError("Tool name was not given to duplicate")
    # Check new tool name to duplicate to has been given
    if new_tool_name is None:
        raise AttributeError("New tool name was not given to name duplicate")
    # Check the tool name is not protected
    if new_tool_name in xjtools.const.PROTECTED_TOOL_NAMES:
        raise ValueError(f"'{new_tool_name}' is a protected tool name, try using another name")

    # Check file exists, and new duplicate name is not already taken
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.abspath(os.path.join(
        root_dir,
        xjtools.const.TOOLS_DIR,
        f"{tool_name}.py"
    ))
    filepath_new = os.path.abspath(os.path.join(
        root_dir,
        xjtools.const.TOOLS_DIR,
        f"{new_tool_name}.py"
    ))

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Tool '{tool_name}' does not exist")
    if os.path.exists(filepath_new):
        raise FileExistsError(f"There is already a tool called '{new_tool_name}', " \
            "choose another new name")

    # If no errors raised, duplicate the tool
    with open(filepath_new, "w", encoding="utf-8") as newf:
        with open(filepath, "r", encoding="utf-8") as oldf:
            for index, line in enumerate(oldf):
                newline = None
                re_find_scriptname = re.match(xjtools.const.REGEXES["name"], line)
                re_find_date = re.match(xjtools.const.REGEXES["date"], line)
                re_find_argparser = re.match(xjtools.const.REGEXES["argparser"], line)
                if re_find_scriptname:
                    newline = f"{re_find_scriptname.groups()[0]}" \
                        f"{new_tool_name}{re_find_scriptname.groups()[2]}\r\n"
                    output_msg(f">> Found scriptname on line {index+1}, replace with:")
                    output_msg(f"'{newline.rstrip()}'")
                elif re_find_date:
                    newdate = datetime.datetime.now().strftime(xjtools.const.DATETIME_FORMAT)
                    newline = f"{re_find_date.groups()[0]}{newdate}\r\n"
                    output_msg(f">> Found date on line {index+1}, replace with:")
                    output_msg(f"'{newline.rstrip()}'")
                elif re_find_argparser:
                    newline = f"{re_find_argparser.groups()[0]}" \
                        f"{new_tool_name}{re_find_argparser.groups()[2]}\r\n"
                    output_msg(f">> Found argparser on line {index+1}, replace with:")
                    output_msg(f"'{newline.rstrip()}'")
                else:
                    newline = line
                newf.write(newline)


def delete_tool(tool_name: str):
    """Deletes the selected tool from the ../tools/ dir
       by moving it into a subfolder ../tools/.deleted

    Args:
        tool_name (str): tool name to delete

    Raises:
        AttributeError: missing or invalid argument given
        FileNotFoundError: tool to delete not found
    """
    # Check tool name param has been given
    if tool_name is None:
        raise AttributeError("Tool name was not given to delete")

    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{tool_name}.py"
    filepath = os.path.abspath(os.path.join(root_dir, xjtools.const.TOOLS_DIR, filename))

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Tool '{tool_name}' does not exist")

    confirmation = input(f"{xjtools.const.PRINT_PREFIX} " \
        f"Are you sure you want to delete '{tool_name}'? [Y/n]: ")
    if confirmation.lower() == "y":
        deleted_dir = os.path.join(root_dir, xjtools.const.TOOLS_DIR, ".deleted")
        if not os.path.exists(deleted_dir):
            os.mkdir(deleted_dir)

        deleted_filepath = os.path.abspath(os.path.join(deleted_dir, filename))
        deleted_file_index = 0
        while os.path.exists("{deleted_filepath}_{deleted_file_index}"):
            deleted_file_index += 1

        shutil.move(filepath, f"{deleted_filepath}_{deleted_file_index}")
        output_msg(f"Done: Tool '{tool_name}' has been moved to the '.deleted' directory")


def output_msg(msg: str):
    """Manages output messages from the library

    Args:
        msg (str): the message to output
    """
    print(f"{xjtools.const.PRINT_PREFIX} {msg}")

if __name__ == "__main__":
    output_msg("Error: xjtools is a library, and can't be called directly.")
