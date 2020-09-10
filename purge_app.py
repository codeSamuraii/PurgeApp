#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
purge_app.py
© Rémi Héneault (@codesamuraii)
https://github.com/codesamuraii
"""
import plistlib
from os import remove, geteuid
from pathlib import Path
from shutil import rmtree
from sys import argv


# Common directories where app-related data is
SEARCH_DIRECTORIES_USER = [
    Path.home() / "Library",
    Path("/Library"),
    Path("/System/Library"),
    Path("/Users/Shared"),
]

SEARCH_DIRECTORIES_ROOT = [
    Path('/bin'),
    Path('/etc'),
    Path('/var'),
]


class SkipSignal:
    def __init__(self):
        self.skip = False

    def on(self):
        self.skip = True

    def yes(self):
        if self.skip is True:
            self.skip = False
            return True
        else:
            return False


def read_plist(app_path):
    """Reads the app .plist file and returns a set containing the the 'clues' concerning the app."""
    try:
        plist_path = Path(app_path, "Contents/Info.plist").resolve(strict=True)
    except FileNotFoundError:
        # The name of the app
        print("  Unable to read app informations. Search will be based on name only.")
        return {plist_path.parents[1].stem}

    plist_content = plistlib.loads(plist_path.read_bytes())

    # Relevant identifiers to read
    identifiers = ["CFBundleIdentifier", "CFBundleName", "CFBundleSignature"]
    relevant_infos = {plist_content.get(id) for id in identifiers}

    # Removing not found values
    relevant_infos.discard(None)
    relevant_infos.discard('????')

    return relevant_infos


def get_identifiers(path_to_app):
    hints = read_plist(path_to_app)
    to_use = set()

    print("\n- Identifiers found:")
    for hint in hints:
        if input("  > {}\t\tuse? (Y/n) ".format(hint)) not in {'N', 'n'}:
            to_use.add(hint)

    if not to_use:
        print("\nx No data to use. Quitting.")
        exit()
    else:
        return to_use


def check_dir(dir_path, hints, skip_signal):
    """Recursive generator to walk through directories and check for hints."""
    try:
        dir_content = list(dir_path.iterdir())
    except PermissionError:
        return

    for node in dir_content:
        try:
            if any(h in node.name for h in hints):
                yield node

                if skip_signal.yes():
                    break

            elif node.is_dir() and not node.is_symlink():
                yield from check_dir(node, hints, skip_signal)
        except PermissionError:
            continue


def scan(search_directories, hints, skip_signal):
    """Recursively search in provided directories for hints."""
    for directory in search_directories:
        for match in check_dir(directory, hints, skip_signal):
            yield match


def run(path_to_app):
    """Main function."""
    if geteuid() == 0:
        print("- Running as root, extending search parameters.")
        search_directories = SEARCH_DIRECTORIES_USER + SEARCH_DIRECTORIES_ROOT
    else:
        search_directories = SEARCH_DIRECTORIES_USER

    print("- Reading app informations...\n  > {}".format(path_to_app))
    hints = get_identifiers(path_to_app)

    print("\n- Searching for app-related data (may take a while)...")
    skip_signal = SkipSignal()
    for match in scan(search_directories, hints, skip_signal):
        action = input("  > '{}' (y/N/skip) ".format(str(match)))

        if action in {'y', 'Y'}:
            try:
                if match.is_dir():
                    rmtree(str(match))
                else:
                    remove(str(match))
            except PermissionError:
                print("    Permission error, unable to delete.")
                continue

        elif action in {'s', 'S'}:
            skip_signal.on()
            print("  Skipped: '{}'".format(match.parent))

    # Removing the app itself
    if input("\n- Delete the app itself ? [y/N] ") in {'y', 'Y'}:
        rmtree(path_to_app)
        print("* Done !")


# NOTE: Really bad design, will use argparse afterwards
if __name__ == '__main__':
    if len(argv) < 2:
        print("Usage: purge_app.py PATH_TO_APP.app")
        exit()

    run(argv[1])
