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
    navigators = serializeraw.create_pagetextnavigators_frompath(
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
    navigators = serializeraw.create_pagetextnavigators_frompath(
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
    navigators = serializeraw.create_pagetextnavigators_frompath(
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
    navigators = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.BACHELOR111_PDF),
        pages=page,
    )
    nav = utila.select_page(navigators, page)
    # TODO: REMOVE WITH EXTRACT MOVING FOOTER
    footer = nav.between(0.77, 0.95)
    assert len(footer) == 5, str(footer)
    return footer


SAMPLE = [
    (8, iamraw.BoundingBox.from_str("130.91 668.55 540.00 704.02")),
    (6, iamraw.BoundingBox.from_str("358.45 605.24 480.47 625.77")),
    (7, iamraw.BoundingBox.from_str("467.46 650.40 540.00 667.51")),
    (3, iamraw.BoundingBox.from_str("409.67 513.88 540.01 558.02")),
    (4, iamraw.BoundingBox.from_str("550.0 513.88 600.0 558.02")),
    (5, iamraw.BoundingBox.from_str("304.91 587.31 534.01 607.84")),
    (2, iamraw.BoundingBox.from_str("77.38 216.25 121.22 230.47")),
    (0, iamraw.BoundingBox.from_str("303.26 40.18 308.74 54.44")),
    (1, iamraw.BoundingBox.from_str("77.38 102.67 534.62 206.45")),
]


@pytest.fixture
def navigator() -> texmex.PageTextNavigator:
    dimension = document_size([item for _, item in SAMPLE])
    result = texmex.PageTextNavigator(dimension)
    for item, position in SAMPLE:
        result.insert(bounding=position, text=item, style=None)
    assert len(result) == len(SAMPLE)
    return result


def document_size(items):
    dimension = utila.rectangle_max(items)
    return (dimension[2], dimension[3])
