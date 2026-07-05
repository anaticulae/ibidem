# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import ibidem.config
import ibidem.strategy.highnote
import ibidem.utils


def work(
    text: str,
    textpositions: str,
    horizontals: str,
    pages=None,
) -> str:
    # load
    horizontals = serializeraw.load_horizontals(
        horizontals,
        pages=pages,
        width_min=ibidem.config.FOOTER_SEPARATOR_WIDTH_MIN,
    )
    ptns = serializeraw.ptn_fromfile(
        text,
        textpositions,
        pages=pages,
        state=ibidem.config.VISIBLE,
    )
    ptns = ibidem.utils.rotate_ifrequired(ptns)
    strategy = ibidem.strategy.highnote.HighnoteStrategy(
        horizontals=horizontals,
        ptns=ptns,
    )
    result = strategy.result()
    dumped = serializeraw.dump_headerfooter(result)
    return dumped
