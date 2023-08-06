import argparse
import json
import os
from pathlib import Path
from typing import Dict

from dircrawler import crawl

from ._config import parse_config
from ._structure import restructure


def main():
    parser = argparse.ArgumentParser(description='format file directory files')
    parser.add_argument('command', choices=['restructure'])
    parser.add_argument('-p', '--path', help='home path', default=os.getcwd())
    parser.add_argument('-c', '--config', help='config file location. default is config.json', default='config.json')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    parser.add_argument('-m', '--move', help='moves files instead of default copy', action='store_true')
    parser.add_argument('-s', '--start', help='start depth of file search', default=None)
    parser.add_argument('-e', '--end', help='end depth of file search', default=None)

    args = parser.parse_args()

    if args.command == 'restructure':
        _restructure_from_args(args)


def _restructure_from_args(args):
    raw_config: Dict[str, str] = {}
    with Path(args.config).open('r') as f:
        raw_config = json.load(f)

    parsed_config = parse_config(raw_config)
    print(parsed_config)
    files, dirs = crawl(args.path, start_depth=args.start if args.start else 0,
                        end_depth=args.end if args.end else -1)
    print(files)
    restructure(parsed_config, args.path, files, args.verbose, args.move)