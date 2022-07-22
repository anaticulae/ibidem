# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math

import configo
import iamraw
import texmex.navigator
import utila

import footnote.parser.plain
import footnote.strategy
import footnote.strategy.moving.judge
import footnote.strategy.moving.run


class PlainMovingStrategy(footnote.strategy.moving.run.MovingStrategy):

    def __init__(
        self,
        horizontals: iamraw.PagesWithHorizontalList,
        ptns: texmex.PageTextNavigators,
    ):
        super().__init__(
            horizontals,
            ptns,
            footnote_strategy=footnote.parser.plain.parse,
            invalid_footer=invalid_footer,
        )

    def result(self):
        detected = super().result()
        if disable_strategy(detected):
            detected = []
        return detected

    def report(self) -> footnote.strategy.FootnoteExtractionReport:
        # TODO: Avoid multiple computation, require  concept.
        detected = self.result()
        report = footnote.strategy.moving.judge.analyze(detected)
        return report


STRATEGY_ERROR_MAX = configo.HolyTable(items=[
    (0, 0),
    (5, 1),
    (10, 2),
    (20, 4),
    (50, 8),
    (100, 15),
],)


def disable_strategy(footers) -> bool:
    """The plain moving strategy is only used in unique cases. Mostly
    this strategy detects uncompleted footnotes which are no valid
    footnotes. Therefore we require a strategy to disable these wrong
    results.

    It is not common to have many invalid footnotes. As a result of this
    fact, we disable this strategy if the errors are to high.
    """
    if not footers:
        return False
    nonumber_count = 0
    for page in footers:
        nonumber = [item for item in page.footer.notes if item.number < 0]
        if nonumber:
            nonumber_count += 1
    max_error = STRATEGY_ERROR_MAX(len(footers))
    if nonumber_count > max_error:
        return True
    return False


BOTTOM_BORDER = configo.HV_PERCENT_PLUS(default=60)

FOOTER_COUNT_MIN = configo.HolyTable(
    items=(
        (BOTTOM_BORDER, 10),
        (0.8, 2),
        (0.9, 1),
        (1.0, 0),
    ),
    strategy=utila.Strategy.LINEARISE,
)


def invalid_footer(begin, content) -> bool:
    """Check if potential footer contain too few content and therefore
    can't be a footer."""
    # TODO: The distance between footer line and footer content is very
    # high in bachelor128. Think about to change invalidation method. May
    # introduce high distance check?
    mincount = FOOTER_COUNT_MIN(begin)
    mincount = math.floor(mincount)
    if len(content) < mincount:
        utila.debug(f'invalid footer: {content}')
        return True
    return False
