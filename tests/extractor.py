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
import serializeraw

import tests


def footer(source: str, td, mp, pages: str = ':'):
    cmd = f'-i {power.link(source)}  --pages={pages}'
    tests.run(cmd, mp=mp)
    headerpath = iamraw.path.footnote_result(td.tmpdir)
    loaded = serializeraw.load_headerfooter(headerpath)
    return loaded
