"""
libs.strings

By default, uses `en-us.json` file inside the `strings` top-level folder.

If the language changes, set the `libs.strings.default_locale` and run `libs.strings.refresh()`
"""

import json

default_locale = "en-us"
cached_strings = {}


def refresh():
    global cached_strings
    with open(f"strings/{default_locale}.json") as f:
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


refresh()
