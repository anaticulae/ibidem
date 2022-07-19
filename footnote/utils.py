# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import configo
import german
import utila

HIGHNOTE_RISE_MIN = configo.HV_FLOAT_PLUS(default=3.0)

NUMBER = utila.compiles(r'\[?(\d{1,4})\]?')


def parse_footnote_number(text: str) -> int:
    """\
    >>> parse_footnote_number('[133]')
    133
    """
    matched = NUMBER.match(text)
    if not matched:
        utila.error(f'could not convert to int: {text}')
        return text
    result = int(matched[1])
    return result


NUMBER_TEXT = utila.compiles(
    r"""
    \[?
    (?P<number>\d{1,4})
    \]?
    (?!
        (   # do not detect 229ff. as footnote
            \d{0,4}(f|p){1,2}\.
        )
        |
        (   # do not detect 2.1.3 as footnote
            \.\d{1,2}\.
        )
        |
        (   # do not detect date as footnote 18.06.2019)
            \d{1,2}\.\d{1,2}\.\d{4}|
            \d{4}\.\d{1,2}\.\d{1,2}
            # TODO: SUPPORT MORE TYPES OF DATES
        )
        |
        (
            \d{0,4}[;,:/)\]]  # Yorkstr.\n40; vgl. Einwohnerbuch der Stadt Erfurt
        )
    )
    [ ]{0,4}
    (?P<text>.{3,})
""",
    flags=(re.X | re.MULTILINE | re.DOTALL),
)


def search_footnote(text):
    r"""\
    >>> search_footnote('61 UNDP HDR 2007/2008, S.\n229ff. Die Weltfinanzkrise 2008-9'
    ... '\n62 In der Tat wurde der Begriff bereits')
    (61, 'UNDP HDR 2007/2008, S.\n229ff. Die Weltfinanzkrise 2008-9\n62 In der Tat wurde der Begriff bereits')
    >>> search_footnote('229ff. Die Weltfinanzkrise 2008-9')
    (-1, '229ff. Die Weltfinanzkrise 2008-9')
    >>> search_footnote('18.06.2019)')
    (-1, '18.06.2019)')
    """
    matched = NUMBER_TEXT.match(text)
    if not matched:
        number, content = -1, text
    else:
        number, content = int(matched['number']), matched['text']
    return number, content


def ishighnote(style, text: str) -> bool:
    highnote_occurs = style.rise >= HIGHNOTE_RISE_MIN
    if not highnote_occurs:
        return False
    text = text[style.start:style.end].strip()
    if NUMBER.match(text):
        return True
    return False


def hyperlink_improve(text: str) -> str:
    r"""\
    >>> hyperlink_improve('found at https://aur.\narchlinux.org/trusted-user/TUbylaws.html. There')
    'found at https://aur.archlinux.org/trusted-user/TUbylaws.html. There'

    Do not fail on empty line.
    >>> hyperlink_improve('http://www.google.de\n\nhello.')
    'http://www.google.de\n\nhello.'

    Regression test, do not fail on empty lines
    >>> hyperlink_improve(' \nfirst\nsecond')
    'first\nsecond'
    """
    # TODO: MOVE TO GERMAN?
    splitted = text.strip().splitlines()
    if len(splitted) == 1:
        # no merging required
        return text
    result = splitted[0]
    for item in splitted[1:]:
        lastitem = result.split()[-1]
        if not german.links(lastitem):
            result += utila.NEWLINE + item
            continue
        firstitem = item.split()
        if not firstitem:
            # newline
            result += utila.NEWLINE
            continue
        # select first word
        firstitem = firstitem[0]
        # skip last char to avoid single word with sentence sign
        firstitem = firstitem[0:-1]
        if any(char in firstitem for char in '/-.:'):
            # merge link
            result += item
            continue
        # no link to merge
        result += utila.NEWLINE + item
    return result
