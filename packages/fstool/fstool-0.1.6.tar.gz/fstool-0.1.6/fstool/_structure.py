import re
import shutil
from pathlib import Path

from .external.regexfind import SubsetGraph, default_tests


def restructure(config: dict, home: str, files: list = [], verbose: bool = False, move: bool = True):
    home = Path(home)

    graph = SubsetGraph(default_tests)
    for key in config.keys():
        graph.add_regex(key)

    # create Path objects from all files
    files = [Path(i) for i in files]

    # file loop
    for file in files:

        new_file = None

        match = graph.match(str(file.parts[-1]))
        if match:  # if there is a match
            # print(match[0].string)

            match_object = config[match[0].string]
            if match[0].string == match_object['file']:
                new_file = home / Path(match_object['dir']) / Path(file.parts[-1])
            else:
                original_match = re.match(match[0].string, str(file.parts[-1]))
                new_match = re.match(r'.+', match_object['file'])

                try:
                    new_file = home / Path(match_object['dir']) / re.sub(match[0].string, match_object['file'], str(file.parts[-1]))
                except re.error as e:
                    print(f'[ERROR] {file} - {e}')
                # print(new_file)

        # if no new file skip
        if not new_file:
            continue

        # create parent directory
        new_file.parent.mkdir(parents=True, exist_ok=True)

        if verbose:
            print(f'[{"MOVE" if move else "COPY"}] {file} -> {new_file}')

        if not new_file.exists():
            # copy file to new location
            shutil.copy(str(file), str(new_file))
        if move:
            # remove old file
            file.unlink()
