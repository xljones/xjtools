"""
    Script:      lib/xjinstaller.py
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
"""

from app.lib import helpers

# Needs to add to .zshrc/.bashrc
# Needs to install requirements
# python3 -m pip install -r requirements.txt

if __name__ == "__main__":
    helpers._output_msg(
        "Error: xjinstaller.py is a library, and can't be called directly. Try using `cd .. && python3 xjtools.py -h` for help"
    )
