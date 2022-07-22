# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Moving Footer Extraction Step
=============================

Requirements:
    We do not check the header, because it is required, that this header
    is fixed.

Example:

- master/page_72_noimages_toc.pdf
- bachelor/page_111_images_toc.pdf

TODO: Think about header
"""

import iamraw
import texmex.navigator
import utila

import footnote.parser.highnote
import footnote.strategy
import footnote.strategy.moving.finish
import footnote.strategy.moving.judge
import footnote.strategy.moving.separator


class MovingStrategy(footnote.strategy.FootnoteDetectionStrategy):

    def __init__(
        self,
        horizontals: iamraw.PagesWithHorizontalList,
        sizeandborders: iamraw.PageSizeBorderList,
        ptns: texmex.PageTextNavigators,
        footnote_strategy: callable = None,
        invalid_footer: callable = None,
    ):
        super().__init__(
            horizontals,
            sizeandborders,
            ptns,
        )
        self.footnote_strategy = footnote_strategy
        self.invalid_footer = invalid_footer

    def run(self):
        horizontals = footnote.strategy.moving.separator.footer_separator(
            self.horizontals,
            self.pagesize,
        )
        result = []
        for horizontal in horizontals:
            pdfpage = horizontal.page
            ptn = self.datum(pdfpage)[0]
            processed = process_page(
                horizontals=horizontal.content,
                ptn=ptn,
                footnote_strategy=self.footnote_strategy,
                invalid_footer=self.invalid_footer,
            )
            if processed.footer is None:
                continue
            result.append(processed)
        return result

    def result(self):
        detected = self.run()
        utila.verbose('footer before merge:')
        utila.verbose(detected)
        utila.verbose()
        result = footnote.strategy.moving.finish.merge_footer_pages(detected)
        utila.verbose('footer after merge:')
        utila.verbose(result)
        utila.verbose()
        result = footnote.strategy.moving.judge.last(result)
        utila.verbose('footer after last:')
        utila.verbose(result)
        utila.verbose()
        return result

    def report(self) -> footnote.strategy.FootnoteExtractionReport:
        # TODO: Avoid multiple computation, require  concept.
        detected = self.result()
        result = footnote.strategy.moving.judge.report(detected)
        return result


def process_page(
    horizontals,
    ptn: texmex.NavigatorMixin,
    footnote_strategy: callable = None,
    invalid_footer: callable = None,
) -> iamraw.PageContentFooterHeader:
    # determine start of footer
    footer = None
    # check PAGENUMBR RAW? OR INHERIT FROM PTN?
    bottomed = footnote.strategy.moving.separator.select_footer_line(
        horizontals,
        pagewidth=ptn.width,
        pageheight=ptn.height,
    )
    if bottomed is not None:
        footer = extract_footer(
            bottomed,
            ptn=ptn,
            footnote_strategy=footnote_strategy,
            invalid_footer=invalid_footer,
        )
    result = iamraw.PageContentFooterHeader(
        footer=footer,
        page=ptn.page,
    )
    return result


def extract_footer(
    footerstart: float,
    ptn: texmex.NavigatorMixin,
    footnote_strategy: callable = None,
    invalid_footer: callable = None,
) -> iamraw.MovingFooterInformation:
    if footnote_strategy is None:
        footnote_strategy = footnote.parser.highnote.parse
    begin = utila.roundme(footerstart / ptn.height)
    content = ptn.after(
        begin,
        selector=texmex.navigator.SelectBounding.BOTTOM,
    )
    if invalid_footer and invalid_footer(begin, content):
        utila.debug(f'invalid footer on page {ptn.page}: {content}')
        return None
    # splitted by highnotes
    footnotes = footnote_strategy(
        content=content,
        width=ptn.width,
        pagenumber=ptn.page,
    )
    if nonumber(footnotes):
        return None
    if not footnotes:
        # no footnotes parsed, therefore do not return MovingFooterInformation
        return None
    lastnote_bounding = footnotes[-1].bounding
    if lastnote_bounding:
        end = utila.roundme(lastnote_bounding[3] / ptn.height)
        end += 0.02  # a little offset to avoid under estimating
    else:
        end = 1.0
        utila.error(f'missing last note bounding: {footnotes[-1]}')
    footer = iamraw.MovingFooterInformation(
        begin=begin,
        end=end,
        notes=footnotes,
    )
    return footer


NONUMBER = (-1, '-1')


def nonumber(footnotes) -> bool:
    if not footnotes:
        return False
    counted = len([item for item in footnotes if item.number in NONUMBER])
    if not counted:
        return False
    if counted >= 2:
        return True
    return False
