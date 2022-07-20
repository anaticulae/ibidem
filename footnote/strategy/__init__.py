# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""The `footer` module extract the footnote area out of pdf-pages.

There are four different strategies:

- MovingStrategy
- PlainMovingStrategy

The strategy run these different strategies and use a judgement-unit to
decide which result is the best. In some cases the best strategy changes
from page to page.

As a result we have `FooterInformation` with additional data.

decider_footnote:
    As a later step the **decider** program judges about footer and
    gives advices to the user about failures and possible improvements.
"""

import abc
import collections
import dataclasses
import typing

import iamraw
import serializeraw
import texmex
import utila

import footnote.config


@dataclasses.dataclass  # pylint:disable=R0903
class FootnoteExtractionReport:
    pass


class FootnoteDetectionStrategy(abc.ABC):
    # TODO: Relative or absolute result dimension?

    def __init__(
        self,
        horizontals: iamraw.PagesWithHorizontalList,
        sizeandborders: iamraw.PageSizeBorderList,
        ptns: texmex.PageTextNavigators,
    ):
        assert isinstance(horizontals, typing.List), str(horizontals)
        self.horizontals = horizontals
        self.sizeandborders = sizeandborders
        self.ptns = ptns

        self.result__ = {}

        self.post_init()

    def post_init(self):
        """Run after __init__"""

    def result(self) -> iamraw.PageContentFooterHeaders:
        raise NotImplementedError()

    def report(self) -> FootnoteExtractionReport:
        """Return meta data to determined `result`.

        The main propose of this report is to have a better view why the
        algorithm produces this given result.
        """
        raise NotImplementedError()

    def pagesize(self, pagenumber) -> tuple:
        """Determine `pageheight` of current `page` in `pixel`.

        Args:
            pagenumber(int): page of pdf document
        Returns:
            pageheight if pageheight exists
            None if pageheight not exists
        """
        selected = utila.select_page(
            self.sizeandborders,
            page=pagenumber,
        )
        if selected is None:
            return (595.28, 841.89)
        return (selected.size.width, selected.size.height)


def create_strategy(
    path: str,
    strategy: FootnoteDetectionStrategy,
    pages=None,
):
    horizontals = serializeraw.load_horizontals(
        path,
        pages=pages,
        width_min=footnote.config.FOOTER_SEPARATOR_WIDTH_MIN,
    )
    sizeandborders = serializeraw.load_pageborders(
        path,
        pages=pages,
    )
    ptn = serializeraw.ptn_frompath(
        path,
        pages=pages,
    )
    result = strategy(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        ptns=ptn,
    )
    return result


def remove_duplication(items: list) -> list:
    """In some cases more than one potential header or footer are
    detected for one page. This method judges the problem and select the
    `best` result.

    Args:
        items: list of `PageContentFooterHeader`
    Returns:
        sorted list without page duplications
    """
    source = collections.defaultdict(list)
    for item in items:
        source[item.page].append(item)

    result = [multijudgement(item) for item in source.values()]

    result = sorted(result, key=lambda x: x.page)
    return result


def multijudgement(judges):
    # TODO: Strategy how to judge multiple matches
    # BIGGER ONE, ITEM OF BIGGER CLUSTER?

    def count_item(item):
        return int(item.footer is not None) + int(item.header is not None)

    current = judges[0]
    count = count_item(current)
    for item in judges[1:]:
        cur_count = count_item(item)
        if cur_count < count:
            continue
        current = item
        count = cur_count
    return current


def strategies():
    import footnote.strategy.moving.run  # pylint:disable=redefined-outer-name
    import footnote.strategy.plainmoving
    # TODO: Automate collection
    result = [
        footnote.strategy.moving.run.MovingStrategy,
        footnote.strategy.plainmoving.PlainMovingStrategy
    ]
    return result
