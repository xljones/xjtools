# my-tools
Collection of small tools and scripts used daily

Add the following to `~/.zshrc`, or `~/.bashrc` depending on zsh or bash terminal use:
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

To create a new tool (from anywhere):
```
tools new <tool_name>
```

To edit a tool, call (from anywhere):
```
tools edit <tool_name>
```

To call a tool for use (from anywhere):
```
tools <tool_name> [optional_arguments]
```
