# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import utilo

import footnote.parser.textraw
import tests.extractor
import tests.fixtures.footnotes


@pytest.mark.parametrize('example', [
    pytest.param(tests.fixtures.footnotes.FOOTNOTES,),
    pytest.param(tests.fixtures.footnotes.FOOTNOTES_SECOND,),
])
def test_footenote_parse_notes(example):
    raw, expected_footnotes = example[0], example[1]
    parsed = footnote.parser.textraw.parse(raw)
    assert len(parsed) == expected_footnotes


def test_footenote_parse_notes_multiline():
    raw = tests.fixtures.footnotes.FOOTNOTES_SECOND[0]
    parsed = footnote.parser.textraw.parse(raw)
    assert len(parsed) == 23, len(parsed)

    assert parsed[0].number == 1
    assert parsed[0].text == ('Aus Grnden der besseren Lesbarkeit wird hier '
                              'und im Folgenden ausschlielich die maskuline '
                              'Form verwendet, wobei immer beide '
                              'Geschlechter gemeint sind.')
    assert parsed[-1].number == 23


def test_master98_page10(td, mp):
    extracted = tests.extractor.footer(
        hoverpower.MASTER098_PDF,
        td,
        mp,
        pages='10',
    )
    footer_ = utilo.select_page(extracted, 10).footer
    notes = footer_.notes
    assert len(notes) == 1
    firstnote_text = notes[0].text.strip()
    # ensure that page number is not merged to note text
    assert firstnote_text.endswith('16)'), firstnote_text


def test_bachelor028p2(td, mp):
    """The hyperlinks produces blue horizontal lines.

    After fixing rawmaker, these horizontal lines does not occur anymore
    and footnote detection works fine.
    """
    extracted = tests.extractor.footer(
        hoverpower.BACHELOR028_PDF,
        td,
        mp,
        pages='2',
    )
    footnotes = extracted[0].footer
    assert len(footnotes) == 6


def test_bachelor078p44p45(td, mp):
    """Merge single footnote over two pages."""
    extracted = tests.extractor.footer(
        hoverpower.BACHELOR078_PDF,
        td,
        mp,
        pages='44,45',
    )
    footnotes = extracted[0].footer.notes
    assert len(footnotes) == 1
    merged = footnotes[0].text
    assert merged.endswith('werden.')


def test_bachelor078p44_footnote_bounding(td, mp):
    """Verify bounding produced by highnote strategy."""
    extracted = tests.extractor.footer(
        hoverpower.BACHELOR078_PDF,
        td,
        mp,
        pages='44',
    )[0]
    firstnote = extracted.footer.notes[0].bounding
    width, height = utilo.rect_width(firstnote), utilo.rect_height(firstnote)
    assert width > 350
    assert height > 40, '4 lines of 10pt text'
