# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import iamraw
import utilo

import ibidem.layout
import ibidem.utils

FOOTNOTE_TEXT_LENGTH_MIN = configos.HV_INT_PLUS(default=len('ebd.'))


def parse(
    content: list,
    width: float = 594.0,
    pagenumber: int = None,
) -> list:
    """\
    Args:
        content(list): content of footnote area
        width(float): width in pixel of current page. As default use DINA4.
        pagenumber(int): pdf raw page number
    Returns:
        List of parsed footnotes
    """
    # append newline to improve merge result
    content = append_newline(content)
    grouped = ibidem.layout.group_footnote_area(content)
    result = []
    for group in grouped:
        parsed = parse_group(group, width=width, pagenumber=pagenumber)
        if not parsed:
            continue
        result.append(parsed)
    return result


def parse_group(group, width: int, pagenumber: int) -> iamraw.FootNoteRaw:
    number, note = group
    has_highnote = number is not None
    if has_highnote:
        x0 = number.bounding[0]
        # TODO: REPLACE WITH DUE PAGE SIZE FORMATS
        if x0 >= ibidem.layout.FOOTNOTE_X0_MAX(width):
            # potential highnote is located too right
            return None
    if len(note.text) < FOOTNOTE_TEXT_LENGTH_MIN:
        utilo.debug(f'footnote too short: {note.text}')
        return None
    notenumber = None
    if has_highnote:
        notenumber = ibidem.utils.parse_footnote_number(number.text)
    if not note.text.strip():
        utilo.error(f'could not parse footnote: {number}, no text content')
        return None
    bounding = tuple(note.bounding) if note.bounding else None
    bounding_number = tuple(number.bounding) if has_highnote else None
    text = ibidem.utils.hyperlink_improve(note.text)
    text = utilo.normalize_text(text, strips=True)
    # TODO: GO MORE BACK TO ORIGIN
    raw = number.text + note.text if has_highnote else note.text
    parsed = iamraw.FootNoteRaw(
        bounding=bounding,
        bounding_number=bounding_number,
        number=notenumber,
        page=pagenumber if pagenumber is not None else -1,
        raw=raw,
        raw_number=number.text.strip() if has_highnote else None,
        style=(number.style if has_highnote else None, note.style),
        style_number=number.style if has_highnote else None,
        style_text=note.style,
        text=text,
    )
    return parsed


def append_newline(lines):
    for line in lines:
        line.text += utilo.NEWLINE
        line.style.content[-1].end += 1
    return lines
