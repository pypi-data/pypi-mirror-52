#!/usr/local/bin/python3
"""
Author       : weaming
Created Time : 2019-04-01 21:41:57

Fuzzy path

environments:
    FZPATH_FILES : also list files (default list only directories)
    ROOT: the root directory to list
"""
import sys
import os
from filetree import File

version = '0.1'
FZPATH_FILES = os.getenv("FZPATH_FILES")


def find_path(F: File, prefixs, found: list, depth_total, depth_current):
    """
    [
        (aa, [
            (ba, [...]),
            (bb, [...]),
        ]),
        (ab, [
            (ba, [...]),
            (bb, [...]),
        ]),
    ]
    """
    # print(prefixs, depth_current, depth_total)
    if not prefixs:
        # not None
        return found
    for X in F.dirs:
        if X.basename[0].lower() == prefixs[0].lower():
            vv = find_path(X, prefixs[1:], [], depth_total, depth_current + 1)
            # check whether not matched
            if vv is None:
                continue
            v = [X.basename, vv]
            found.append(v)

    if FZPATH_FILES:
        # file.files is []
        for X in F.files:
            if X.basename[0].lower() == prefixs[0].lower():
                vv = find_path(X, prefixs[1:], [], depth_total, depth_current + 1)
                # check whether not matched
                if vv is None:
                    continue
                found.append([X.basename, vv])

    if (depth_current < depth_total) and not found:
        # propagate None to ignore not matched list
        return None
    return found


def print_result(result):
    for name, x in result or []:
        if x:
            print_result([[os.path.join(name, y1), y2] for y1, y2 in x])
        else:
            print(name)


def main():
    prefixs = sys.argv[1] if len(sys.argv) >= 2 else ''
    result = find_path(
        File(os.path.expanduser(os.path.expandvars(os.getenv('ROOT', '.')))),
        prefixs,
        [],
        len(prefixs),
        0,
    )
    print_result(result)


if __name__ == '__main__':
    main()
