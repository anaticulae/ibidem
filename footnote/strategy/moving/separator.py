# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import utila

import footnote.layout

FOOTER_SEPARATOR_COUNT_MIN = configo.HV_INT_PLUS(default=10)

# distance from top to bottom
BOTTOM_BORDER = configo.HV_PERCENT_PLUS(default=30)


def footer_separator(horizontals, pagesize: callable) -> list:
    """Remove invalid horizontals as a product of hyperlink printer in
    footnotes which creates an invalid footnote line.

    Use nereast line to document common footnote line.
    """
    flat = utila.flatten_content(horizontals)
    # TODO: EXTRACT FOOTNOTES WITH DIFFERENT FOOTER LINES AND SELECT THE
    # BEST ONE.
    flat = valid_footer_separators(
        flat,
        pagewidth=pagesize(0)[0],
        pageheight=pagesize(0)[1],
        bottom_border=BOTTOM_BORDER,
    )
    if len(flat) < FOOTER_SEPARATOR_COUNT_MIN:
        # dissable mode selector for to few horizontals
        return horizontals
    x0 = utila.mode(utila.roundme([item.box[0] for item in flat], digits=0))
    x1 = utila.mode(utila.roundme([item.box[2] for item in flat], digits=0))
    horizontals = [
        iamraw.PageContentHorizontals(
            content=nearest_line(page.content, x0, x1),
            page=page.page,
        ) for page in horizontals
    ]
    return horizontals


def select_footer_line(
    horizontals,
    pagewidth,
    pageheight,
    bottom_border=BOTTOM_BORDER,
) -> float:
    filtered = valid_footer_separators(
        horizontals,
        pagewidth,
        pageheight,
        bottom_border,
    )
    # determine y-level
    bottomed = max(
        (item.box.y0 for item in filtered),
        default=None,
    )
    return bottomed


def valid_footer_separators(
    horizontals,
    pagewidth,
    pageheight,
    bottom_border,
):
    footer_start = pageheight * bottom_border
    # skip horizontals which are located too top
    filtered = [item for item in horizontals if item.box.y0 >= footer_start]
    # potential footer is located too right
    x0_max = footnote.layout.FOOTNOTE_X0_MAX(pagewidth)
    x1_max = footnote.layout.FOOTNOTE_X1_MAX(pagewidth)
    good_x0 = [item for item in filtered if item.box.x0 <= x0_max]
    good_x0x1 = [
        item for item in filtered
        if item.box.x0 <= x0_max and item.box.x1 <= x1_max
    ]
    if not good_x0x1:
        return good_x0
    return good_x0x1


def nearest_line(horizontals, x0, x1) -> list:
    # TODO: IMPROVE THIS, REQUIRE BETTER SELECTOR TO HANDLE VERY LONG
    # FOOTNOTES.
    horizontals = [item for item in horizontals if item.box[1] > 250.0]
    if not horizontals:
        return []
    best = horizontals[0]
    for horizontal in horizontals[1:]:
        current = utila.norm(best.box[0], best.box[2], x0, x1)
        new = utila.norm(horizontal.box[0], horizontal.box[2], x0, x1)
        if new > current:
            continue
        best = horizontal
    return [best]
