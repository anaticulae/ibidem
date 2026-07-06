# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import ibidem
import tests
import tests.conftest

ARCHIVE = utilo.join(ibidem.ROOT, 'tests/expected', exist=True)


@pytest.mark.parametrize(
    'source',
    utilotest.test_resources(tests.conftest.RESOURCES),
)
@utilotest.nightly
def test_validate_all(source, td, mp):
    Evaluate(
        source=source,
        pages=':',
        expected=None,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(
        hoverpower.DISS143_PDF, '20:26', 'diss143page20', id='diss143p20'),
    pytest.param(hoverpower.DISS480_PDF, '4,5', 'diss480p4p5',
                 id='diss480p4p5'),
])
@utilotest.nightly
def test_validate_selected(source, pages, expected, td, mp):
    utilotest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=pages,
        expected=expected,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilotest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, mp):
        super().__init__(
            program=functools.partial(
                tests.run,
                mp=mp,
            ),
            step='',
            pages=pages,
            source=hoverpower.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=serializeraw.load_footnotes,
            convert_source=False,
            index=expected,
        )

    def raw(self, value) -> str:
        footnotes = utilo.flatten_content(value)
        footnotes = [rawline(item) for item in footnotes]
        result = utilo.NEWLINE.join(footnotes)
        return result


def rawline(note) -> str:
    result = '     '
    if note.raw_number is not None:
        result = str(note.number).zfill(4) + ' '
    result += utilo.normalize_text(note.text.strip())
    return result
