import sys
import pathlib
import argparse


def get_cli_args():
    parser = argparse.ArgumentParser(
        prog='purgeapp',
        formatter_class=argparse.RawTextHelpFormatter,
        description='''Find and clean all files related to an app.\n
                    \rBy default, you will be asked each time if a file is to be deleted.
                    \r\~ You may skip and not remove a directory's content with the `s` option when asked.
                    \r\~ On the contrary, you can delete all files in that folder by using the `a` option.''', \
    )
    source = parser.add_argument_group('app', 'path or name of the app')
    source.add_argument('--path', '-p', type=str, nargs='+', help="path to the app (eg. '/Applications/Axx.app')")
    source.add_argument('--app', '-a', type=str, nargs='+', help="name of the app to remove (eg. 'Spotify')")
    parser.add_argument('--dry', '-d', action='store_true', help="only list files found - no action")
    parser.add_argument(dest='either', type=str, nargs='*')
    return parser.parse_args()


def _parse_unknown(unknown):
    print(unknown)

def main():
    arguments = get_cli_args()
    dry_run = arguments.dry
    paths = arguments.path
    names = arguments.app
    unknown = _parse_unknown(arguments.either)
    print(arguments)








if __name__ == '__main__':
    sys.exit(main())
