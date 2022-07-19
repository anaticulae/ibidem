# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import texmex
import utila


def rotate_ifrequired(navigators, sizeandborders=None):
    if not sizeandborders:
        return navigators
    if isinstance(sizeandborders, str):
        if not utila.exists(sizeandborders):
            utila.error('missing size and borders: pagenumber')
            return navigators
        pages = tuple(page.page for page in navigators)
        sizeandborders = serializeraw.load_pageborders(
            content=sizeandborders,
            pages=pages,
        )
    result = []
    for ptn in navigators:
        pagesize = utila.select_page(sizeandborders, page=ptn.page)
        if pagesize is None:
            # empty navigator or only a part of ptn is extracted
            continue
        pagesize = pagesize.size
        if iswidepage(pagesize):
            ptn = texmex.rotate_left(ptn)
        result.append(ptn)
    return result


def iswidepage(navigator) -> bool:
    return navigator.width > navigator.height


def isrightpage(pdf_pagenumber: int) -> bool:
    """What pdf page is the left side?

    The first page is the right page?
    """
    # TODO: REQUIRE SMART ALTERNATIVE
    if utila.iseven(pdf_pagenumber):
        return True
    return False
