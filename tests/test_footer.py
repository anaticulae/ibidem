# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw.path
import pytest
import serializeraw
import utilo
import utilotest

import footnote.feature.result
import footnote.strategy.moving.run
import tests
import tests.extractor


# TODO: CHECK 25
@pytest.mark.parametrize('strategy, expected_results', [
    (footnote.strategy.moving.run.MovingStrategy, 0),
])
@utilotest.requires(hoverpower.DOCU027_PDF)
def test_footerheader_detectionstategy(
    strategy,
    expected_results,
):
    """Check that different strategies work proper with given resources

    TODO: SEE DUPLICATION test_judgement_strategy_quality?"""
    source = hoverpower.link(hoverpower.DOCU027_PDF)
    horizontals = serializeraw.load_horizontals(source)
    ptn = serializeraw.ptn_frompath(source)
    process = strategy(
        horizontals=horizontals,
        ptns=ptn,
    )
    result = process.result()
    assert len(result) == expected_results, 'not enough footer and header'


@utilotest.longrun
@utilotest.requires(hoverpower.MASTER072_PDF)
def test_master72_extract(td, mp):
    outdir = td.tmpdir
    cmd = f'-i {hoverpower.link(hoverpower.MASTER072_PDF)}  -o {outdir} --pages=3'
    tests.run(cmd, mp=mp)
    headfoot = serializeraw.load_headerfooter(iamraw.path.footnote_result(outdir))  # yapf:disable
    footnotes = headfoot[0].footer.notes
    assert len(footnotes) == 6, str(footnotes)
    first = utilo.normalize_whitespaces(footnotes[0].text)
    assert first.startswith('Aus Gründen der besseren Lesbarkeit'), first


def test_homework18(td, mp):
    extracted = tests.extractor.footer(
        hoverpower.HOME018_PDF,
        td,
        mp,
        pages='3:17',
    )
    content = utilo.flat([item.footer.notes for item in extracted])
    assert len(content) == 94, len(content)


@utilotest.longrun
def test_master110(td, mp):
    """This document does not contain any footnotes."""
    extracted = tests.extractor.footer(
        hoverpower.MASTER110_PDF,
        td,
        mp,
        pages='0:50',
    )
    assert not extracted


def test_master99p8(td, mp):
    extracted = tests.extractor.footer(
        hoverpower.MASTER099_PDF,
        td,
        mp,
        pages='8',
    )
    footer = extracted[0].footer.notes[0].text.strip()
    footer = utilo.normalize_whitespaces(footer)
    assert footer.startswith('Näheres')
    assert footer.endswith('nachgelesen werden.')


@utilotest.nightly
def test_master155p107(td, mp):
    """No footer on page107."""
    extracted = tests.extractor.footer(
        hoverpower.MASTER155_PDF,
        td,
        mp,
        pages='0:110',
    )
    assert not utilo.select_page(extracted, 107)


@utilotest.nightly
def test_master127(td, mp):
    extracted = tests.extractor.footer(
        hoverpower.MASTER127_PDF,
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
    footnotes = utilo.flat([item.notes for item in footers])
    assert len(footnotes) == 135  # VALIDATED


@utilotest.longrun
def test_master075(td, mp):
    extracted = tests.extractor.footer(
        hoverpower.MASTER075_PDF,
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
