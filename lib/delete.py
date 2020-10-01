'''
    Script:      lib/delete.py
    Description: Deletes the selected tool from the ../tools/ dir
                 by moving it into a subfolder ../tools/.deleted
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
'''

import argparse
import os
import sys
import shutil

def _delete_tool(tool_name):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{0}.py".format(tool_name)
    filepath = os.path.join(root_dir, "tools", filename)

    if not os.path.exists(filepath):
        print("Error: Tool '{0}' does not exist".format(tool_name))
        exit(1)
    else:
        confirmation = input("Are you sure you want to delete '{0}'? [Y/n]: ".format(tool_name))
        if confirmation.lower() == "y":
            deleted_dir = os.path.join(root_dir, "tools", ".deleted")
            if not os.path.exists(deleted_dir):
                os.mkdir(deleted_dir)

            deleted_filepath = os.path.join(deleted_dir, filename)
            deleted_file_index = 0
            while os.path.exists("{0}_{1}".format(deleted_filepath, deleted_file_index)):
                deleted_file_index += 1

            shutil.move(filepath, "{0}_{1}".format(deleted_filepath, deleted_file_index))
            print("Done: Tool '{0}' has been moved to the '.deleted' directory".format(tool_name))

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='lib/delete.py')
    p.add_argument("tool_name")
    args = p.parse_args()

    _delete_tool(args.tool_name)
