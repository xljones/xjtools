# my-tools
Collection of small tools and scripts used daily, along with a small framework for quickly creating new tools, and editing current ones.

## Installation
1. Clone this repository
2. Add the following to `~/.zshrc`, or `~/.bashrc` depending on zsh or bash terminal use:
```bash
# function to call the py tool if exists with arguments
tools() {
  # If no arguments given, jump straight to the tools folder
  if [ -z "$1" ]; then
    cd ~/GitHub/my-tools
  # if arguments are given, try and run the script with additional arguments given
  else
    FILE=~/GitHub/my-tools/$1.py
    if test -f "$FILE"; then
      python3 $FILE ${@:2}
    else
      echo "Error: Tool not found"
    fi
  fi
}
```

## Usage
The following command can be run from anywhere on your computer if you have installed the alias in the installation instructions.
### List the tools
```bash
tools list
```
produces the following output
```
$ tools list
+-------+---------+-----------------------------------------------+
| Tool  | Version | Description                                   |
+-------+---------+-----------------------------------------------+
| list  |  1.0.0  | List all of the scripts in this directory     |
| upper |  1.0.0  | Convert any following arguments to upper case |
| edit  |  1.0.0  | Edit a tool in this directory                 |
| new   |  1.0.0  | Create a new tool in this directory           |
+-------+---------+-----------------------------------------------+
```
### To call a tool for use
```
tools <tool_name> [optional_arguments]
```
### Create a new tool:
```
tools new <tool_name>
```
### Edit a tool
By default this opens in Atom. If this is not installed you will need to modify this script
```
tools edit <tool_name>
```
