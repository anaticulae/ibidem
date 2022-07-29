#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Verify expected headlines to determine expected results which are not
fully correct and are a candidat for improving.
"""

import utila


def quality(path):
    print(path)
    files = utila.file_list(path, absolute=True)
    for item in files:
        content = utila.file_read(item)
        parsed = parse_file(content)
        if not parsed:
            continue
        if not error(parsed):
            continue
        utila.error(item)


def parse_file(content: str) -> list:
    result = []
    for line in content.splitlines():
        line = line.strip()
        result.append(line.split(maxsplit=1)[0])
    return result


def error(items):
    try:
        items = [int(item) for item in items]
    except ValueError:
        return True
    grouped = utila.groupby_diff(items)
    if not grouped:
        return False
    if grouped[0][0] == -1:
        return True
    return False


if __name__ == "__main__":
    ROOT = utila.join(utila.path_parent(__file__), 'expected')
    quality(ROOT)
