# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import utila

import footnote.layout
import footnote.utils


def parse(content: list, width: float = 594.0, pagenumber: int = None) -> list:
    collected = prepare(content, pagenumber)
    result = []
    # parse footnote
    for multiline in collected:
        parsed = parse_group(multiline, width=width, pagenumber=pagenumber)
        if not parsed:
            continue
        result.append(parsed)
    return result


def parse_group(
    multiline: list,
    width: float,
    pagenumber: int,
) -> iamraw.FootNoteRaw:
    x0 = multiline[0].bounding[0]  # first line x0
    if x0 >= footnote.layout.FOOTNOTE_X0_MAX(width):
        # potential highnote is located too right
        return None
    raw = utila.NEWLINE.join([item.text.strip() for item in multiline])
    raw = footnote.utils.hyperlink_improve(raw)
    number, content = footnote.utils.search_footnote(raw)
    text = utila.normalize_text(
        content,
        normalize_spaces=True,
        strips=True,
    )
    bounding = utila.rect_max([item.bounding for item in multiline])
    bounding_number = tuple(multiline[0].bounding)
    parsed = iamraw.FootNoteRaw(
        bounding=bounding,
        bounding_number=bounding_number,
        number=number,
        style=None,
        page=pagenumber if pagenumber is not None else -1,
        text=text,
        raw=raw,
        raw_number='' if number == -1 else str(number),
    )
    return parsed


def prepare(content: list, pdfpage: int) -> list:
    neighbors = footnote.layout.connect_neighbors(content)
    collected = [merges(neighbor, pdfpage) for neighbor in neighbors]
    result = utila.flat(collected)
    return result


MERGE_LINE_MIN = configo.HV_INT_PLUS(default=len('1. Ebd.'))


def merges(content, pdfpage: int):
    if not content:
        return []
    collected = [[content[0]]]
    # merge multiple lines
    for line in content[1:]:
        if new_footnote(line.text, pdfpage):
            collected.append([line])
        else:
            collected[-1].append(line)
    return collected


FOOTNOTE_NUMBER_MAX = configo.HolyTable(
    items=(
        (0, 40),
        (20, 200),
        (30, 300),
        (40, 500),
        (70, 500),
        (500, 1500),
        (1000, 3000),
    ),
    strategy=utila.Strategy.LINEARISE,
)


def new_footnote(
    text,
    pdfpage: int,
    merge_line_min: int = MERGE_LINE_MIN,
) -> bool:
    text = text.strip()
    matched = footnote.utils.NUMBER_TEXT.match(text)
    if not matched:
        return False
    if len(text) < merge_line_min:
        return False
    footnote_number_max = FOOTNOTE_NUMBER_MAX[pdfpage]
    if int(matched['number']) > footnote_number_max:
        return False
    return True
