#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
purge_app.py
© Rémi Héneault (@codesamuraii)
https://github.com/codesamuraii
"""
import inspect
import plistlib
from os import remove
from pathlib import Path
from shutil import rmtree
from sys import argv

# Common directories where app-related data is
SEARCH_DIRECTORIES = [
    Path.home() / "Library",
    Path("/Library"),
    Path("/System/Library"),
    Path("/Users/Shared"),
    Path("/private"),
    Path('/bin'),
    Path('/etc'),
    Path('/var')
]


def read_plist(app_path):
    """This function returns a set containing the the 'clues' concerning the app."""
    try:
        plist_path = Path(app_path, "Contents/Info.plist").resolve(strict=True)
    except FileNotFoundError:
        # The name of the app
        if input("[!] Couldn't read app information, continue with the name only ? [y/N] ") in {'y', 'Y'}:
            return {plist_path.parents[1].stem}
        else:
            exit()

    plist_content = plistlib.loads(plist_path.read_bytes())

    # Relevant identifiers to read
    identifiers = ["CFBundleIdentifier", "CFBundleName", "CFBundleSignature"]
    relevant_infos = {plist_content.get(id) for id in identifiers}

    # Removing not found values
    relevant_infos.discard(None)
    relevant_infos.discard('????')

    return relevant_infos


def check_dir(dir_path, hints):
    """Recursive generator to walk through directories and check for hints."""
    try:
        dir_content = list(dir_path.iterdir())
    except PermissionError:
        return

    for node in dir_content:
        try:
            if any(h in node.name for h in hints):
                yield node

            elif node.is_dir() and not node.is_symlink():
                yield from check_dir(node, hints)
        except PermissionError:
            continue


def scan(path_to_app):
    """Returns a set of paths that may be related the the app."""

    hints = read_plist(path_to_app)
    print("* Identifiers :")
    for hint in hints:
        print(" - {}".format(hint))

    results = set()

    for directory in SEARCH_DIRECTORIES:
        for match in check_dir(directory, hints):
            results.add(match)

    return results


# NOTE: Really bad design, will use argparse afterwards
if __name__ == '__main__':
    if len(argv) < 2:
        print("Usage: purge_app.py PATH_TO_APP.app")
        exit()

    print("* Searching for app-related data...")
    matches = scan(argv[1])
    print("* Found {} potential leftovers. Delete :".format(len(matches)))

    for match in matches:
        if input("  — {} [y/N] ".format(str(match))) in {'y', 'Y'}:
            if match.is_dir():
                rmtree(str(match))
            else:
                remove(str(match))

    # Removing the app itself
    if input(" * Delete the app itself ? [y/N] ") in {'y', 'Y'}:
        rmtree(argv[1])

        print("* Done !")

    else:
        print("* Aborting.")
