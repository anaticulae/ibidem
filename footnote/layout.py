# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import math
import typing

import configo
import iamraw
import texmex
import utila

import footnote.utils

HIGHNOTE_VERTICAL_LINE_DIFF_MAX = configo.HV_FLOAT_PLUS(default=15.0)

FOOTNOTE_X0_MAX = configo.HolyTable(items=(
    (440, 100),  # TODO: US Letter?
    (550, 150),  # DINA4
))
FOOTNOTE_X1_MAX = configo.HolyTable(items=(
    (440, 100 + 200),  # TODO: US Letter?
    (550, 150 + 200),  # DINA4
))

FOOTNOTE_RATE_MIN = configo.HV_PERCENT_PLUS(default=50)


def group_footnote_area(content) -> list:
    connected_neighbors = connect_neighbors(content)
    if not connected_neighbors:
        return []
    result = []
    has_highnote = 0
    for group in connected_neighbors:
        splitted = split_textinfo(group)
        if any(high for high, _ in splitted):
            has_highnote += 1
        merged = merge_online(splitted)
        result.extend(merged)
    result = merge_after(result)
    rate = utila.rate_rel(has_highnote, len(connected_neighbors))
    if rate < FOOTNOTE_RATE_MIN:
        if len(result) == 1:
            return result
        utila.debug(f'no highnotes: {rate} detected, skip footnote result')
        utila.verbose(result)
        return []
    return result


def merge_after(items: list) -> list:
    """Make merger more robust against false formatted footnotes.

    Merge footnote text which is under highnote on the left side.

    See:
        - bachelor041a p14
        - master091b   p54
    """
    if not items:
        return []
    result = [items[0]]
    for highnote, content in items[1:]:
        if highnote is not None:
            # normal footnote
            result.append((highnote, content))
            continue
        highnote_before = result[-1][0] is not None
        if highnote_before:
            # merge them
            for item in content.style.content:
                item.start += len(result[-1][1].text)
                item.end += len(result[-1][1].text)
            result[-1][1].text += content.text
            result[-1][1].style.content.extend(content.style.content)
            continue
        # footnote without highnote
        result.append((None, content))
    return result


def connect_neighbors(items) -> list:
    if not items:
        return []
    result = [[items[0]]]
    for item in items[1:]:
        before = result[-1][-1]
        if connected(before.bounding, item.bounding):
            result[-1].append(item)
        else:
            result.append([item])
    return result


def split_textinfo(content) -> list:
    """Split text by `hightnote` and preserve TextInfo.

    Go line by line from top to bottom. Collect lines till highnote
    occurs. If highnote occurs merge content and add to result.

    Returns:
        list of a tuple of highnote and content
    """
    assert isinstance(content, list), type(content)
    result = []
    highnote = None
    collected = []
    for item in content:
        for style in item.style.content:
            if ishighnote(style, item.text):
                if collected:
                    result.append((highnote, union(collected)))
                    collected = []
                style = style.copy()
                highnote = texmex.TextInfo(
                    text=item.text[style.start:style.end],
                    style=style,
                    bounding=char_bounding(item.bounding, item.text, style),
                )
                style.start = 0
                style.end = len(highnote.text)
            else:
                bounding = iamraw.split_x(
                    item.bounding,
                    style.start,
                    len(item.text),
                )
                collected.append(TextChunk(item.text, style, bounding))
    if highnote or collected:
        # there is always content left at the end
        result.append((highnote, union(collected)))
    return result


def merge_online(items) -> list:
    """Ensure that high notes are located on a vertical line.

    Therefore we have to ignore highnotes which are located inside the
    text and not part of the text flow.

    Steps:
        1. Determine the most left highnotes
        2. Adjust highnotes on most left one
        3. Merge other highnotes into text
    """
    if not items:
        return []
    result = []
    # skip None-Highnotes => if item
    with_highnote = [high.bounding.x0 for high, _ in items if high]
    mostleft = min(with_highnote) if with_highnote else None
    high, collected = None, []
    for highnote, content in items:
        if not highnote:
            result.append((None, content))
            continue
        diff = math.fabs(highnote.bounding.x0 - mostleft)
        if diff > HIGHNOTE_VERTICAL_LINE_DIFF_MAX:
            # highnote in content
            collected.append(
                shrink_tostyle(
                    highnote.text,
                    highnote.style,
                    bounding=highnote.bounding,
                ))
            collected.extend([
                shrink_tostyle(content.text, style, bounding=content.bounding)
                for style in content.style
            ])
        else:
            # new highnotes
            if high:
                result.append((high, union(collected)))
            high = highnote
            collected = [
                shrink_tostyle(content.text, style, bounding=content.bounding)
                for style in content.style
            ]
    notempty = collected or high
    if notempty:
        # do not add empty items
        result.append((high, union(collected)))
    return result


# increase word diff at the start of the line to merge huge gap between
# footnote number and footnote text.
LEFTRIGHT_DIFF_MAX = configo.HolyTable(items=(
    (0, 40),
    (100, 40),
    (120, 40),
    (150, 30),
    (200, 20),
    (300, 20),
    (400, 20),
    (500, 20),
))

SAMEORIGIN_DIFF_MAX = configo.HV_FLOAT_PLUS(default=35.0)

SAMELINE_DIFF_MAX = configo.HV_FLOAT_PLUS(default=5.0)

UNDERFIRST_DIFF_MAX = configo.HV_FLOAT_PLUS(default=10.0)


def connected(first: tuple, second: tuple) -> bool:
    leftright_diff_max = LEFTRIGHT_DIFF_MAX(first.x0)
    # words are neighbors
    leftright = utila.near(
        first.x1,
        second.x0,
        diff=leftright_diff_max,
    )
    # plus indention
    sameorigin = utila.near(
        first.x0,
        second.x0,
        diff=SAMEORIGIN_DIFF_MAX,
    )
    sameline = utila.near(
        first.y0,
        second.y0,
        diff=SAMELINE_DIFF_MAX,
    )
    underfirst = utila.near(
        first.y1,
        second.y0,
        diff=UNDERFIRST_DIFF_MAX,
    )
    result = (leftright or sameorigin) and (sameline or underfirst)
    return result


@dataclasses.dataclass
class TextChunk:
    text: str = None
    style: texmex.TextStyle = None
    bounding: iamraw.BoundingBox = None


TextChunks = typing.List[TextChunk]


def shrink_tostyle(text: str, style, bounding=None) -> TextChunk:
    text = text[style.start:style.end]
    style = style.copy()
    style.start, style.end = 0, len(text)
    # TODO: ADD BOUNDING ADJUSTMENT, IN THE CURRENT CASE, WE DO NOT SHRINK
    # THE BOUNDING
    return TextChunk(text, style, bounding)


def union(chunks: TextChunks) -> texmex.TextInfo:
    raw = ''
    content = []
    for chunk in chunks:  # pylint:disable=W0612
        start = len(raw)
        raw += chunk.text[chunk.style.start:chunk.style.end]
        end = len(raw)
        section_style = chunk.style.copy()
        section_style.start, section_style.end = start, end
        content.append(section_style)
    bounding = [item.bounding for item in chunks if item.bounding]
    bounding = utila.rect_max(bounding) if bounding else None
    result = texmex.TextInfo(
        text=raw,
        style=texmex.TextStyle(content=content),
        bounding=bounding,
    )
    return result


def char_bounding(
    bounding: iamraw.BoundingBox,
    text: str,
    style: texmex.TextStyle,
) -> iamraw.BoundingBox:
    width = bounding.x1 - bounding.x0
    char_width = width / len(text)
    x0 = bounding.x0 + char_width * style.start
    x1 = bounding.x0 + char_width * style.end
    result = iamraw.BoundingBox(x0, bounding.y0, x1, bounding.y1)
    return result


HIGHNOTE_RISE_MIN = configo.HV_FLOAT_PLUS(default=3.0)


def ishighnote(style, text: str) -> bool:
    highnote_occurs = style.rise >= HIGHNOTE_RISE_MIN
    if not highnote_occurs:
        return False
    text = text[style.start:style.end].strip()
    if footnote.utils.NUMBER.match(text):
        return True
    return False
