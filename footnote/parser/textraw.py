# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This module parses :class:`iamraw.FootNote` out of raw text data.

There are 2 supported types of footnotes:

- raw text:

  - "1 Aus Gründen der besseren Lesbarkeit wird hier und im "

- bibliography:

  - "5 s. Berg 2013: 2"
  - "6 Gero von Randow, zeit.de, 19.1.2007"


.. todo::

  - TODO: FOR FURTHER ANALYSIS WE REQUIRE DIFFERENT FOOTER LINE ANALYZER


  ? we have to use a combination of font rise and maybe textual grammar ?
"""

import iamraw
import utila


def parse(content: str, pagenumber: int = None):
    assert isinstance(content, str), type(content)
    result = []
    for raw in footnote_split(content):
        parsed = parse_group(raw, pagenumber)
        if not parsed:
            continue
        result.append(parsed)
    return result


def parse_group(raw: str, pagenumber: int) -> iamraw.FootNoteRaw:
    number, text = raw.split(maxsplit=1)
    if not text.strip():
        utila.error(f'could not parse footnote: {number}, no text content')
        return None
    text = utila.normalize_text(text)
    footnote = iamraw.FootNoteRaw(
        number=int(number),
        text=text,
        raw=raw,
        page=pagenumber if pagenumber is not None else -1,
    )
    return footnote


FOOTNOTE_NUMBER = utila.compiles(r"""
    ^
    (
        \d{1,4}|
        \[\d{1,4}\]|
        \(\d{1,4}\)
    )
    [ ]{1,5}
""")


def footnote_split(raw: str) -> list:
    """Split footnotes into chunks.

    A empty newline or a starting footnote([int, whitespace]) marks the
    ending of a multiline footnote.

    Example:
    .. code-block:: none

        ...End of some Text.

        1 I am the first note
        2 I am a
        very long
        multiline note.

        I am a lonely newline which will not pass.
        3 But i will pass the test

        30 Helm

        Start of some text..
    """
    result = []
    for item in raw.splitlines():
        item = item.strip()
        if not item:
            # empty newline separates list elements from text
            result.append(None)
        elif FOOTNOTE_NUMBER.match(item):
            # match line start pattern
            result.append([item])
        elif result and result[-1]:
            # ensure to have valid predecessor
            result[-1].append(item)
        else:
            # TODO: INVESTIGATE HERE
            pass
    joined = [' '.join(item) for item in result if item]
    return joined
