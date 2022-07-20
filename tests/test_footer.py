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
import tests
import tests.extractor


# TODO: CHECK 25
@pytest.mark.parametrize('strategy, expected_results', [
    (footnote.strategy.moving.run.MovingStrategy, 0),
])
def test_footer_footerheader_detectionstategy(
    strategy,
    expected_results,
):
    """Check that different strategies work proper with given resources

    TODO: SEE DUPLICATION test_footer_judgement_strategy_quality?"""
    source = power.link(power.DOCU027_PDF)
    horizontals = serializeraw.load_horizontals(source)
    sizeandborders = serializeraw.load_pageborders(source)
    ptn = serializeraw.ptn_frompath(source)
    process = strategy(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        ptns=ptn,
    )
    result = process.result()
    assert len(result) == expected_results, 'not enough footer and header'


@utilatest.longrun
def test_footer_master72_extract(td, mp):
    outdir = td.tmpdir
    cmd = f'-i {power.link(power.MASTER072_PDF)}  -o {outdir} --pages=3'
    tests.run(cmd, mp=mp)

    headfoot = serializeraw.load_headerfooter(
        iamraw.path.footnote_result(outdir))
    footnotes = headfoot[0].footer.notes
    assert len(footnotes) == 6, str(footnotes)

    first = utila.normalize_whitespaces(footnotes[0].text)
    assert first.startswith('Aus Gründen der besseren Lesbarkeit'), first


def test_footer_homework18(td, mp):
    extracted = tests.extractor.footer(
        power.HOME018_PDF,
        td,
        mp,
        pages='3:17',
    )
    content = utila.flatten([item.footer.notes for item in extracted])
    assert len(content) == 94, len(content)


@utilatest.longrun
def test_footer_master110(td, mp):
    """This document does not contain any footnotes."""
    extracted = tests.extractor.footer(
        power.MASTER110_PDF,
        td,
        mp,
        pages='0:50',
    )
    assert not extracted


def test_footer_master99_page8(td, mp):
    extracted = tests.extractor.footer(
        power.MASTER099_PDF,
        td,
        mp,
        pages='8',
    )
    footer = extracted[0].footer.notes[0].text.strip()
    footer = utila.normalize_whitespaces(footer)
    assert footer.startswith('Näheres')
    assert footer.endswith('nachgelesen werden.')


@utilatest.nightly
def test_footer_master155_page107(td, mp):
    """No footer on page107."""
    extracted = tests.extractor.footer(
        power.MASTER155_PDF,
        td,
        mp,
        pages='0:110',
    )
    assert not utila.select_page(extracted, 107)


@utilatest.nightly
def test_footer_master127(td, mp):
    extracted = tests.extractor.footer(
        power.MASTER127_PDF,
        td,
        mp,
        pages=':',
    )
    footers = [
        item.footer
        for item in extracted
        if isinstance(item.footer, iamraw.MovingFooterInformation)
    ]
    assert len(footers) == 73  # VALIDATED
    footnotes = utila.flatten([item.notes for item in footers])
    assert len(footnotes) == 135  # VALIDATED


@utilatest.longrun
def test_footer_master075(td, mp):
    extracted = tests.extractor.footer(
        power.MASTER075_PDF,
        td,
        mp,
        pages=':',
    )
    footers = [
        item.footer
        for item in extracted
        if isinstance(item.footer, iamraw.MovingFooterInformation)
    ]
    assert not footers
