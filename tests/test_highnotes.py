# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import texmex
import utilotest

import ibidem.parser.highnote
import ibidem.parser.textraw


@utilotest.longrun
def test_footnote_parse_footer_with_highnotes(master89page7):
    parsed = ibidem.parser.highnote.parse(master89page7)
    assert len(parsed) == 1, parsed


@utilotest.longrun
def test_footnote_highnotes_oneline_with_intention(bachelor111page10):
    parsed = ibidem.parser.highnote.parse(bachelor111page10)
    assert len(parsed) == 3, str(parsed)
    notes = [item.number for item in parsed]
    assert notes == [3, 4, 5], str(notes)


# yapf:disable
ITEMS = [
    texmex.TextInfo(**{
        'text': '8Data Length Code\n',
        'bounding': iamraw.BoundingBox(x0=86.85, y0=623.17, x1=171.64, y1=636.74),
        'style': texmex.TextStyle(content=[
            texmex.CharStyle(start=0, end=1, size=7.57, rise=4.29, font=773298602),
            texmex.CharStyle(start=1, end=18, size=9.96, rise=0.0, font=904427114)
        ]),
        'bounding_mean': 12.01,
        },),
    texmex.TextInfo(**{
        'text': '9\n',
        'bounding': iamraw.BoundingBox(x0=86.85, y0=635.54, x1=90.64, y1=644.82),
        'style': texmex.TextStyle(content=[
            texmex.CharStyle(start=0, end=2, size=7.57, rise=0.0, font=773298602)
        ]),
        'bounding_mean': 9.28,
        },),
    texmex.TextInfo(**{
        'text': '„Die Hamming-Distanz d(C) eines Codes C gibt den minimalen Abstand zwischen zwei gültigen,\n',
        'bounding': iamraw.BoundingBox(x0=91.14, y0=636.88, x1=514.1, y1=655.01),
        'style': texmex.TextStyle(content=[
            texmex.CharStyle(start=0, end=1, size=9.96, rise=0.0, font=904427114),
            texmex.CharStyle(start=1, end=84, size=9.96, rise=5.9, font=904427114),
            texmex.CharStyle(start=84, end=85, size=9.96, rise=5.92, font=904427114),
            texmex.CharStyle(start=85, end=93, size=9.96, rise=5.9, font=904427114)
        ]),
        'bounding_mean': 12.21,
        },),
]
#yapf:enable

EXPECTED = [
    'Data Length Code',
    '”Die Hamming-Distanz d(C) eines Codes C gibt den minimalen Abstand zwischen zwei gültigen',
]


@pytest.mark.xfail(reason='bad formatted pdf file')
def test_highnotes_prepare():
    # TODO: WE HAVE TO FIX THIS LATER. IT IS A LITTLE BIT COMPLICATED,
    # CAUSE HIGHNOTE/TEXT IS NOT PRINTED CORRECTLY, THEREFORE WE MAY
    # REQUIRE A NEW PARSING STRATEGY.
    parsed = ibidem.parser.highnote.parse(ITEMS)
    lines = [item.text for item in parsed]
    assert lines == EXPECTED
