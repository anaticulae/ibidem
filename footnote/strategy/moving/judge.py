# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses

import configos
import iamraw
import utilo

import footnote.strategy
import footnote.strategy.moving.utils

# relation between detected and empty detected footer to reduce miss detection
WRONG_STRATEGY_EMPTY_FOOTER_FACTOR = configos.HV_PERCENT_PLUS(default=20)

FOOTNOTE_NUMBER_ERROR_MAX = configos.HV_FLOAT_PLUS(default=0.4)


@dataclasses.dataclass
class MovingFooterResultReport(footnote.strategy.FootnoteExtractionReport):
    footer: int = None
    header: int = None
    footer_empty: int = None
    too_many_empty_footer: bool = False


def last(result) -> list:
    numbers = footnote.strategy.moving.utils.footnote_numbers_flat(result)
    if footnote_number_error(numbers):
        utilo.debug('too many footnote number error, skip result')
        utilo.debug(numbers)
        result = []
    return result


def report(detected) -> MovingFooterResultReport:
    detected = judge_detection(detected)
    result = analyze(detected)
    return result


def judge_detection(items):
    """Second analyzing step. Prove that `items` contain a good
    detection result.

    The following things will be checked:

    - (x) selection of correct strategy
    - ( ) quality of extracted footnotes
    """
    reportx = analyze(items)
    # This can happen when using the wrong strategy. If we parse
    # FixedFooter with MovingStrategy, there are a lot of footer
    # which are threated as MovingFooter with Footnote, but this detection
    # is not correct.
    if reportx.too_many_empty_footer:
        return []
    return items


def analyze(results) -> MovingFooterResultReport:
    footer_count = count_footer(results)
    emptyfooter_count = count_empty(results)
    empty_factor = emptyfooter_count / footer_count if footer_count else 0
    too_many_empty_footer = empty_factor >= WRONG_STRATEGY_EMPTY_FOOTER_FACTOR
    # create report
    result = MovingFooterResultReport(
        footer=footer_count,
        footer_empty=emptyfooter_count,
        too_many_empty_footer=too_many_empty_footer,
    )
    return result


def count_footer(items):
    footer = select_footer(items)
    result = len(footer)
    return result


def count_empty(items: iamraw.PageContentFooterHeader) -> int:
    """Count `MovingFooterInformation` which contain a empty `notes` list"""
    footers = [item.footer for item in items if item.footer]
    empty_footnotes = [item for item in footers if not item.notes]
    result = len(empty_footnotes)
    return result


def select_footer(items):
    return [item.footer for item in items if item.footer]


def footnote_number_error(numbers: list) -> bool:  # pylint:disable=R0911
    """\
    >>> footnote_number_error([])
    False
    >>> footnote_number_error([1, 1, 1, 2])
    False
    >>> footnote_number_error([13, -1])
    True
    """
    if len(numbers) < 2:
        return False
    diffed = utilo.diffs(numbers)
    if not diffed:
        return False
    if len(diffed) == 1 and diffed[0] > 0:
        # [13, -1] for example
        return True
    fit, error = utilo.partition(
        key=lambda x: 1 <= x <= 2,
        items=diffed,
    )
    if not error:
        return False
    error_rate = utilo.rate_sum(error, fit)
    if error_rate > FOOTNOTE_NUMBER_ERROR_MAX:
        if footnote.strategy.moving.utils.isendnote(numbers):
            return False
        return True
    return False
