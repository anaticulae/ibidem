# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila
import utilatest

import tests.extractor


@utilatest.longrun
def test_paper18p3(td, mp):
    """Regression test to avoid parsing formula as footnote."""
    extracted = tests.extractor.footer(
        power.PAPER18_PDF,
        td,
        mp,
    )
    assert extracted
    page3 = utila.select_page(extracted, 3)
    # do not interpret this formula as footer
    assert not page3


def test_do_not_merge_pagenumber_footer_bachelor76_page21(td, mp):
    extracted = tests.extractor.footer(
        power.BACHELOR076_PDF,
        td,
        mp,
        pages=21,
    )
    note = utila.select_page(extracted, 21).footer.notes[0]
    note = note.text.strip()  # TODO: remove strip later
    assert note.endswith('Vgl. Schlick, J. et. al.(2014), S.58f.'), str(note)
