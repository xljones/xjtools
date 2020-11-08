# xjtools
Collection of small tools and scripts used daily, along with a small framework for quickly creating new tools, and editing current ones.

## Installation
1. Clone this repository
1. Add the following function to `~/.zshrc`, or `~/.bashrc` depending on zsh or bash terminal use
1. Modify the `PYTHON_INTERPRETER` value if you'd like to use a different Python version.
1. Modify the `INSTALL_DIR` to the directory where the repository has been cloned to.
1. Refresh your zsh/bash environment with `$ source ~/.zshrc` or `$ source ~/.bashrc`
```bash
# xjtools
tools() {
  # xjtools - Configuration start
  PYTHON_INTERPRETER=python3
  INSTALL_DIR=~/GitHub/xjtools
  # xjtools - Configuration end

  TOOLS_DIR=tools
  XJTOOLS=$INSTALL_DIR/xjtools.py

  # If no arguments given, jump straight to the tools folder
  if [ -z "$1" ]; then
    cd $INSTALL_DIR

  # if arguments are given, check if it's a lib command
  else
    if [[ "$1" == "help" ]] then
      $PYTHON_INTERPRETER $XJTOOLS -h
    elif [[ "$1" == "new"       ||
            "$1" == "list"      ||
            "$1" == "edit"      ||
            "$1" == "delete"    ||
            "$1" == "rename"    ||
            "$1" == "duplicate" ]] then
      if test -f "$XJTOOLS"; then
        $PYTHON_INTERPRETER $XJTOOLS ${@:1}
      else
        echo "[xjtools] Error: xjtools.py was not found at $XJTOOLS"
      fi
    else
      FILE=$INSTALL_DIR/$TOOLS_DIR/$1.py
      if test -f "$FILE"; then
        $PYTHON_INTERPRETER $FILE ${@:2}
      else
        echo "[xjtools] Error: tool '$1' not found, try \`tools list\` to find the tool."
      fi
    fi
  fi
}
```

## Usage
The following command can be run from anywhere on your computer if you have installed the alias in the installation instructions.
### List the tools
```bash
$ tools list
```
produces the following output
```
$ tools list
[xjtools] Listing tools found in /Users/xanderjones/GitHub/my-tools/tools
+---+-------------+---------+-----------------------------------------------------+
| # | Tool        | Version | Description                                         |
+---+-------------+---------+-----------------------------------------------------+
| 1 | upper       | 1.0.0   | Convert any following arguments to upper case       |
| 2 | minlink     | 1.0.1   | Convert a Bugsnag long link into useful information |
+---+-------------+---------+-----------------------------------------------------+
```
### Call a tool for use
```bash
$ tools TOOL_NAME [arguments] arguments
```
### Create a new tool
```bash
$ tools new TOOL_NAME
```
### Edit a tool
By default this opens in VSCode. You can modify the value `_EDIT_TOOL` in `./lib/xjconst.py` if you'd like to use another editor.
```bash
tools edit TOOL_NAME
```
### Rename a tool
Renaming a tool will also update the internals to reflect the changes, and up the change date to today
```bash
tools rename TOOL_NAME NEW_NAME
```
### Duplicate a tool
Duplicating a tool is similar to renaming, but won't remove the old script you've copied from.
```bash
tools duplicate TOOL_NAME DUPLICATE_NAME
```
### Delete a tool
This moves the tool into a sub hidden folder called `.deleted`, and appends an index value to the file if there are more than 1 of the same name.
```bash
tools delete TOOL_NAME
```
