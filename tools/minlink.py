'''
    Script:      tools/minlink.py
    Description: Convert a Bugsnag long link into useful information
    Author:      Xander Jones (xander@xljones.com)
    Web:         xljones.com
    Date:        03 Oct 2020
'''

import argparse
import re
import pyperclip

_VERSION = "1.0.1"

def _bugsnag_minify(link):
    re_link = r'^(https?:\/\/app.bugsnag.com)\/([^\/]*)\/([^\/]*)\/([^\/]*)\/([^\/?]*)\??(.*).*$'
    filter_index = 5
    re_match_link = re.match(re_link, link)
    event_id = None

    if re_match_link:
        print("💎  Filters")
        groups = re_match_link.groups()
        for index, match in enumerate(groups[filter_index].split("&")):
            print("├── [{filter_index}][{index}] {match}")
            if match[:8].lower() == "event_id":
                event_id = match
                # strip the event_id to empty string if it doesn't exist.
                if event_id is None:
                    event_id = ""
                else:
                    event_id = "?{event_id}"

        print("💎  Minlink")
        minlink = "{groups[0]}/{groups[1]}/{groups[2]}/{groups[3]}/{groups[4]}{event_id}"
        print("├── [Minlink] {minlink}")
        print("└── Copied to clipboard")
        pyperclip.copy(minlink)
    else:
        print("no match")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description='tools/minlink.py (v{_VERSION})')
    p.add_argument("bugsnag_link", help="The Bugsnag link to get data from")
    a = p.parse_args()

    _bugsnag_minify(a.bugsnag_link)
