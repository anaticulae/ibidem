# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Footer Extraction Step
=============================

TODO:
    what should we do with empty header/footer
"""

import collections

import iamraw
import serializeraw
import utilo


def work(
    xhighnote: str,
    xplain: str,
    pages=None,
) -> str:
    """Extract footer and header area out of horizontal lines.

    Returns:
        Dumped list with top and bottom border, which separates the
        content from the footer and or header, for every page
    """
    highnote = serializeraw.load_headerfooter(
        xhighnote,
        pages=pages,
    )
    plain = serializeraw.load_headerfooter(
        xplain,
        pages=pages,
    )
    # select the best one
    result = judge_strategy((
        highnote,
        plain,
    ))
    validate(result)
    # dump
    dumped = serializeraw.dump_headerfooter(result)
    return dumped


def judge_strategy(
    results: list[iamraw.PageContentFooterHeaders],
) -> iamraw.PageContentFooterHeaders:
    """Decide which results fits best.

    Zip result of different strategies. Sometimes there are multiple
    options, therefore we have to use the priorities below.

    Sources/Concept:

        - MovingFooter:                footer (first prio)
        - Pages:                       footer (second prio)
        - FixedFooter:      header and footer (third prio)
        - Common:           header            (last prio)
        - PlainMoving:

    Args:
        results: lists of `footnote.FootnoteDetectionStrategy`.result
    Returns:
        list of zipped result
    """
    assert results is not None, 'require list of strategy results'
    result = []
    for pdfpage, (
            moving,
            plainmoving,
    ) in utilo.sync_pages(results):
        footer = moving.footer if moving else None
        footer_best = 'moving' if moving else None
        # strategy: moving
        if moving and moving.footer and moving.footer.notes:
            footer = moving.footer
            footer_best = 'moving'
        # strategy: plain
        if not (moving and moving.footer) and plainmoving and plainmoving.footer: # yapf:disable
            # use plain moving only if no other strategy works
            footer = plainmoving.footer
            footer_best = 'plain'
        # log footer best
        if footer_best:
            utilo.verbose(f'footer: {pdfpage} {footer_best}')
        current = iamraw.PageContentFooterHeader(
            footer=footer,
            page=pdfpage,
        )
        result.append(current)

    page_order = [item.page for item in result]
    assert utilo.isascending(page_order), page_order
    return result


def quality(results: list) -> tuple:
    """Determine quality[0.0, 1.0] of every extraction strategy."""
    # count number of page
    pages = set()
    # count result for every strategy
    counter = collections.defaultdict(int)
    for pdfpage, data in utilo.sync_pages(results):
        pages.add(pdfpage)
        for index, item in enumerate(data):
            if not item:
                continue
            counter[index] += 1
    result = tuple(counter[index] / len(pages) if pages else 0
                   for index, _ in enumerate(results))
    return result


def validate(items: list):
    """Validate list of pageable items.

    If some `page` attribute is duplicated, raise ValueError.

    Args:
        items(list): list of objects with <page,content>
    Raises:
        ValueError: if some page attribute is duplicated.
    """
    # TODO: REMOVE AFTER UPGRADING IAMRAW
    counter = collections.Counter()
    for item in items:
        counter[item.page] += 1
    msg = []
    for page, value in counter.most_common():
        if value <= 1:
            continue
        msg.append(f'duplicated page: {page} ({value})')
    if msg:
        raise ValueError(utilo.NEWLINE.join(msg))
