# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utila
import utilatest

import footnote.feature.result
import footnote.strategy.moving.run
import footnote.strategy.plainmoving


def validate_master72(result):
    first_notes = utila.select_page(result, page=3).footer.notes
    assert first_notes[0].number == 1, first_notes[0].number


def validate_bachelor90(result):
    footnotes = flat_footnotes(result)  # pylint:disable=W0612
    numbers = [item.number for item in footnotes]
    assert numbers == utila.rlist(12)


def validate_homework18(result):
    footnotes = flat_footnotes(result)  # pylint:disable=W0612


@pytest.mark.parametrize('source, pages, expected_footer, strategy, validate', [
    pytest.param(
        power.MASTER072_PDF,
        utila.ranged_tuple(20),
        [(3, 6), (6, 3), (7, 2), (8, 4), (9, 1), (10, 4), (11, 3), (12, 2),
         (13, 6), (14, 7), (15, 8), (16, 10), (17, 8), (18, 7), (19, 8)],
        footnote.strategy.moving.run.MovingStrategy,
        validate_master72,
        id='master72pages',
    ),
    pytest.param(
        power.BACHELOR111_PDF,
        utila.ranged_tuple(20),
        [(9, 2), (10, 3), (11, 2), (12, 1), (13, 1), (15, 2), (16, 1), (17, 8),
         (18, 3), (19, 1)],
        footnote.strategy.moving.run.MovingStrategy,
        None,
        id='bachelor111pages',
    ),
    pytest.param(
        power.DOCU027_PDF,
        utila.ranged_tuple(20),
        [],
        footnote.strategy.moving.run.MovingStrategy,
        None,
        id='docu027',
    ),
    pytest.param(
        power.MASTER110_PDF,
        None,
        [],
        footnote.strategy.moving.run.MovingStrategy,
        None,
        id='master110',
    ),
    pytest.param(
        power.DISS178_PDF,
        (22,),
        [(22, 5)],
        footnote.strategy.moving.run.MovingStrategy,
        None,
        id='diss178page22',
    ),
    pytest.param(
        power.HOME018_PDF,
        utila.ranged_tuple(6),
        [(3, 3), (4, 4), (5, 7)],
        footnote.strategy.plainmoving.PlainMovingStrategy,
        validate_homework18,
        id='home18',
    ),
    pytest.param(
        power.BACHELOR090_PDF,
        utila.ranged_tuple(18, 25),
        [(18, 2), (19, 1), (21, 1), (22, 3), (23, 4)],
        footnote.strategy.moving.run.MovingStrategy,
        validate_bachelor90,
        id='bachelor90',
        marks=pytest.mark.xfail(reason='pdf is not printed correctly'),
    ),
])
@utilatest.longrun
def test_footer_moving(
    source,
    pages,
    expected_footer,
    strategy,
    validate,
):
    """Hint: This test is dependend on moving footer strategy. If this
    test fails, may the footer is not extracted correctly. Look at the
    holy value in moving.py:extract_footer."""
    source = power.link(source)
    strategy = footnote.strategy.create_strategy(
        path=source,
        strategy=strategy,
        pages=pages,
    )
    result = strategy.result()

    if validate:
        validate(result)

    footer = [item for item in result if item.footer]
    assert len(footer) == len(expected_footer), footer

    for page, length in expected_footer:
        extracted_footer = utila.select_page(result, page)
        notes = extracted_footer.footer.notes
        assert len(notes) == length, f'on page: {page}'
        assert extracted_footer[1], utila.log_raw(f'has no footer: {page}')


def test_footer_master72pages():
    source = power.link(power.MASTER072_PDF)
    path = iamraw.path.horizontals(source)
    result = serializeraw.load_horizontals(path)
    assert len(result) > 10, str(result)


def flat_footnotes(pages):
    result = []
    for page in pages:
        result.extend(page.footer)
    return result
