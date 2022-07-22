# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import pytest
import serializeraw
import utila
import utilatest

import footnote
import tests

ARCHIVE = utila.join(footnote.ROOT, 'tests/expected', exist=True)

step = lambda x: pytest.param(x, ':', utila.file_name(x), id=utila.file_name(x))


@pytest.mark.parametrize(
    'source',
    utilatest.test_resources(tests.conftest.RESOURCES),
)
@utilatest.nightly
def test_validate_all(source, td, mp):
    Evaluate(
        source=source,
        pages=':',
        expected=None,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.DISS143_PDF, '20:26', 'diss143page20', id='diss143p20'),
    pytest.param(power.DISS480_PDF, '4,5', 'diss480p4p5', id='diss480p4p5'),
])
@utilatest.nightly
def test_validate_selected(source, pages, expected, td, mp):
    Evaluate(
        source=source,
        pages=pages,
        expected=expected,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, mp):
        super().__init__(
            program=functools.partial(
                tests.run,
                mp=mp,
            ),
            step='',
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=serializeraw.load_footnotes,
            convert_source=False,
            index=expected,
        )

    def raw(self, value) -> str:
        footnotes = utila.flatten_content(value)
        footnotes = [rawline(item) for item in footnotes]
        result = utila.NEWLINE.join(footnotes)
        return result


def rawline(note) -> str:
    result = '     '
    if note.raw_number is not None:
        result = str(note.number).zfill(4) + ' '
    result += utila.normalize_text(note.text.strip())
    return result
