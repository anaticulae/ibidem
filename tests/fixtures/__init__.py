# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import texmex
import utila


@pytest.fixture
def master72page14():
    navigators = serializeraw.ptn_frompath(
        power.link(power.MASTER072_PDF),
        pages=14,
    )
    nav = utila.select_page(navigators, 14)
    footer = nav.between(0.8, 0.93)
    assert len(footer) == 7, str(footer)
    return footer


@pytest.fixture
def master89page7():
    page = 7
    navigators = serializeraw.ptn_frompath(
        power.link(power.MASTER089_PDF),
        pages=page,
    )
    nav = utila.select_page(navigators, page)
    footer = nav.between(0.83, 0.95)
    assert len(footer) == 6, str(footer)
    return footer


@pytest.fixture
def master89page19():
    page = 19
    navigators = serializeraw.ptn_frompath(
        power.link(power.MASTER089_PDF),
        pages=page,
    )
    nav = utila.select_page(navigators, page)
    # TODO: REMOVE WITH EXTRACT MOVING FOOTER
    footer = nav.between(0.68, 0.95)
    assert len(footer) == 16, len(footer)
    return footer


@pytest.fixture
def bachelor111page10():
    page = 10
    navigators = serializeraw.ptn_frompath(
        power.link(power.BACHELOR111_PDF),
        pages=page,
    )
    nav = utila.select_page(navigators, page)
    # TODO: REMOVE WITH EXTRACT MOVING FOOTER
    footer = nav.between(0.77, 0.95)
    assert len(footer) == 5, str(footer)
    return footer
