# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""The `footer` module extract the header and footer area out of
pdf-pages.
There are four different strategies:

- FixedFooterStrategy
- MovingFooterStrategy
- PageNumberStrategy
- CommonTextStrategy

The strategy is to run these different strategies and use a
judgement-unit to decide which result is the best. In some cases the best
strategy changes from page to page.

As a result we have the `HeaderInformation` and `FooterInformation` with
additional data. As a further the **decider** program judges about
header and footer and gives advices to the user about failures and
possible improvements.
"""

import abc
import collections
import dataclasses
import typing

import iamraw
import iamraw.path
import serializeraw
import texmex
import utila

import footnote.config


@dataclasses.dataclass  # pylint:disable=R0903
class FooterStrategyReport:
    pass


class FooterHeaderDetectionStrategy(abc.ABC):
    # TODO: Relative or absolute result dimension?

    def __init__(
        self,
        horizontals: iamraw.PagesWithHorizontalList,
        sizeandborders: iamraw.PageSizeBorderList,
        pagetextnavigators: texmex.PageTextNavigators,
    ):
        assert isinstance(horizontals, typing.List), str(horizontals)
        self.horizontals = horizontals
        self.sizeandborders = sizeandborders
        self.pagetextnavigators = pagetextnavigators

        self.result__ = {}

        self.post_init()

    def post_init(self):
        """Run after __init__"""

    def result(self) -> iamraw.PageContentFooterHeaders:
        raise NotImplementedError()

    def report(self) -> FooterStrategyReport:
        """Return meta data to determined `result`. The main propose of
        this report is to have a better view why the algorithm produces
        this given result."""
        raise NotImplementedError()

    def pageheight(self, page) -> int:
        """Determine `pageheight` of current `page` in `pixel`.

        Args:
            page(int): page of pdf document
        Returns:
            pageheight if pageheight exists
            None if pageheight not exists
        """
        selected = utila.select_page(self.sizeandborders, page)
        if selected is None:
            return None
        pageheight = selected.size.height
        return pageheight


def create_strategy(
    path: str,
    strategy: FooterHeaderDetectionStrategy,
    pages=None,
):
    horizontals = iamraw.path.horizontals(path)
    horizontals = serializeraw.load_horizontals(
        horizontals,
        pages=pages,
        width_min=footnote.config.FOOTER_SEPARATOR_WIDTH_MIN,
    )

    sizeandborders = iamraw.path.sizeandborder(path)
    sizeandborders = serializeraw.load_pageborders(sizeandborders, pages=pages)

    navigator = serializeraw.create_pagetextnavigators_frompath(
        path,
        pages=pages,
    )
    result = strategy(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        pagetextnavigators=navigator,
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


def select_footer(items):
    return [item.footer for item in items if item.footer]


def count_footer(items):
    footer = select_footer(items)
    result = len(footer)
    return result


def strategies():
    import footnote.strategy.moving.run  # pylint:disable=redefined-outer-name
    import footnote.strategy.plainmoving
    # TODO: Automate collection
    result = [
        footnote.strategy.moving.run.MovingFooterStrategy,
        footnote.strategy.plainmoving.PlainMovingFooterStrategy
    ]
    return result
