# xjtools
Collection of small tools and scripts used daily, along with a small framework for quickly creating new tools, and editing current ones.

## Installation
1. Clone this repository with `$ git clone https://github.com/xander-jones/xjtools.git`
1. Add the following function to `~/.zshrc`, or `~/.bashrc` depending on zsh or bash terminal use
1. Modify the `PYTHON_INTERPRETER` value if you'd like to use a different Python version.
1. Modify the `INSTALL_DIR` to the directory where the repository has been cloned to.
1. Refresh your zsh/bash environment with `$ source ~/.zshrc` or `$ source ~/.bashrc`

```bash
# xjtools
tools() {
  # xjtools - Configuration start
  PYTHON_INTERPRETER=venv/bin/python
  INSTALL_DIR=~/Git/xljones/xjtools
  APP_DIR=app
  TOOLS_DIR=tools
  # xjtools - Configuration end

  # If no arguments given, jump straight to the tools folder
  if [ -z "$1" ]; then
    cd $INSTALL_DIR

  # if arguments are given, check if it's a lib command
  else
    if [[ "$1" == "help" ]] then
      (cd $INSTALL_DIR && $PYTHON_INTERPRETER -m $APP_DIR -h)
    elif [[ "$1" == "new"       ||
            "$1" == "list"      ||
            "$1" == "edit"      ||
            "$1" == "delete"    ||
            "$1" == "rename"    ||
            "$1" == "duplicate" ]] then
      if test -d "$INSTALL_DIR/$APP_DIR"; then
        (cd $INSTALL_DIR && $PYTHON_INTERPRETER -m $APP_DIR ${@:1})
      else
        echo "[xjtools] Error: module not found at $INSTALL_DIR/$APP_DIR"
      fi
    else
      FILE=$TOOLS_DIR/$1.py
      if test -f "$FILE"; then
        (cd $INSTALL_DIR && $PYTHON_INTERPRETER $FILE ${@:2})
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
