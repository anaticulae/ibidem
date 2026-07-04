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
import serializeraw
import utilotest

import tests


def footer(source: str, td, mp, pages: str = ':'):
    utilotest.fixture_requires(source)
    cmd = f'-i {hoverpower.link(source)}  --pages={pages}'
    tests.run(cmd, mp=mp)
    headerpath = iamraw.path.footnote_result(td.tmpdir)
    loaded = serializeraw.load_headerfooter(headerpath)
    return loaded
