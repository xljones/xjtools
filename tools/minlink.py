"""
    Script:      tools/minlink.py
    Description: Convert a Bugsnag long link into useful information
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        03 Oct 2020
"""

import argparse
import os
import re
import sys

import pyperclip

_VERSION = "1.0.1"


def _bugsnag_minify(link):
    re_link = r"^(https?:\/\/app.bugsnag.com)\/([^\/]*)\/([^\/]*)\/([^\/]*)\/([^\/?]*)\??(.*).*$"
    filter_index = 5
    re_match_link = re.match(re_link, link)
    event_id = None

    if re_match_link:
        print("💎  Filters")
        g = re_match_link.groups()
        for index, match in enumerate(g[filter_index].split("&")):
            print("├── [{0}][{1}] {2}".format(filter_index, index, match))
            if match[:8].lower() == "event_id":
                event_id = match
                # strip the event_id to empty string if it doesn't exist.
                if event_id == None:
                    event_id = ""
                else:
                    event_id = "?{0}".format(event_id)

        print("💎  Minlink")
        minlink = "{0}/{1}/{2}/{3}/{4}{5}".format(
            g[0], g[1], g[2], g[3], g[4], event_id
        )
        print("├── [Minlink] {0}".format(minlink))
        print("└── Copied to clipboard")
        pyperclip.copy(minlink)
    else:
        print("no match")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="tools/minlink.py (v{0})".format(_VERSION))
    p.add_argument("bugsnag_link", help="The Bugsnag link to get data from")
    # p.add_argument('-s', '--string', help='')
    # p.add_argument('-b', '--bool', help='', action='store_true')
    args = p.parse_args()

    _bugsnag_minify(args.bugsnag_link)
