# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex

import footnote.parser.highnote
import footnote.strategy.moving.run


class HighnoteStrategy(footnote.strategy.moving.run.MovingStrategy):

    def __init__(
        self,
        horizontals: iamraw.PagesWithHorizontalList,
        ptns: texmex.PageTextNavigators,
    ):
        super().__init__(
            horizontals,
            ptns,
            footnote_strategy=footnote.parser.highnote.parse,
            invalid_footer=None,
        )
