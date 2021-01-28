'''
    Script:      tools/pwc.py
    Description: Grab the characters of a password at set places in the string
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        15 Jan 2021
'''

import argparse

_VERSION = "1.0.0"

def _get_positional_pw_chars(args):
    if len(args.character_positions) <= 0:
        print("Error: No password character positons were given (see help for more info with `-h`)")
    else:
        print("Getting password characters:")
        for pos in args.character_positions:
            if int(pos) > len(args.password) or int(pos) <= 0:
                print("[{0}] {1}".format(str(pos), "Error: This value is out of range"))
            else:
                print("[{0}] {1}".format(str(pos), args.password[int(pos)-1]))

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='tools/pwc.py (v{0})'.format(_VERSION))
    p.add_argument("password", help="The password to get characters from")
    p.add_argument("character_positions", nargs="*", default=[], help="Space seperated int character positions to get")

    args = p.parse_args()

    _get_positional_pw_chars(args)