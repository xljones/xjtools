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
