# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import pytest
import serializeraw
import texmex
import utilo
import utilotest


@pytest.fixture
def master72page14():
    utilotest.fixture_requires(hoverpower.MASTER072_PDF)
    navigators = serializeraw.ptn_frompath(
        hoverpower.link(hoverpower.MASTER072_PDF),
        pages=14,
    )
    nav = utilo.select_page(navigators, 14)
    footer = nav.between(0.8, 0.93)
    assert len(footer) == 7, str(footer)
    return footer


@pytest.fixture
def master89page7():
    utilotest.fixture_requires(hoverpower.MASTER089_PDF)
    page = 7
    navigators = serializeraw.ptn_frompath(
        hoverpower.link(hoverpower.MASTER089_PDF),
        pages=page,
    )
    nav = utilo.select_page(navigators, page)
    footer = nav.between(0.83, 0.95)
    assert len(footer) == 6, str(footer)
    return footer


@pytest.fixture
def master89page19():
    utilotest.fixture_requires(hoverpower.MASTER089_PDF)
    page = 19
    navigators = serializeraw.ptn_frompath(
        hoverpower.link(hoverpower.MASTER089_PDF),
        pages=page,
    )
    nav = utilo.select_page(navigators, page)
    # TODO: REMOVE WITH EXTRACT MOVING FOOTER
    footer = nav.between(0.68, 0.95)
    assert len(footer) == 16, len(footer)
    return footer


@pytest.fixture
def bachelor111page10():
    utilotest.fixture_requires(hoverpower.BACHELOR111_PDF)
    page = 10
    navigators = serializeraw.ptn_frompath(
        hoverpower.link(hoverpower.BACHELOR111_PDF),
        pages=page,
    )
    nav = utilo.select_page(navigators, page)
    # TODO: REMOVE WITH EXTRACT MOVING FOOTER
    footer = nav.between(0.77, 0.95)
    assert len(footer) == 5, str(footer)
    return footer
