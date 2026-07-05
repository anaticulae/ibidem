# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import resinf
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import footnote
# pylint:disable=W0611
from tests.fixtures import bachelor111page10
from tests.fixtures import master72page14
from tests.fixtures import master89page7
from tests.fixtures import master89page19

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = footnote.PROCESS

RESOURCES = [
    (hoverpower.BACHELOR051_PDF, '0:25'),
    (hoverpower.BACHELOR063_PDF, '0:20'),
    (hoverpower.BACHELOR076_PDF, '0:25'),
    (hoverpower.BACHELOR090_PDF, '0:25'),
    (hoverpower.BACHELOR241_PDF, '0:100'),
    (hoverpower.BOOK173_PDF, '0:100'),
    (hoverpower.DISS178_PDF, '0:30'),
    (hoverpower.DISS218_PDF, '0:100'),
    (hoverpower.DISS264_PDF, '0:50'),
    (hoverpower.DISS273_PDF, '30:60'),
    (hoverpower.DISS287_PDF, '0:100'),
    (hoverpower.DISS406_PDF, '0:75,100:150'),
    (hoverpower.MASTER098_PDF, '0:15'),
    (hoverpower.MASTER099_PDF, '0:30'),
    (hoverpower.MASTER112_PDF, '5,6'),
    (hoverpower.MASTER116_PDF, '50:117'),
    (hoverpower.ORDER009_PDF, '0:10'),
    resinf.todo(
        hoverpower.DISS172_PDF,
        figureo=True,
        tablero=True,
        rawmaker=gennex.CONFIG,
    ),
    resinf.todo(hoverpower.DOCU007_PDF, tablero=True, rawmaker=gennex.CONFIG),
    resinf.todo(hoverpower.MASTER063_PDF, figureo=True),
    hoverpower.BACHELOR028_PDF,
    hoverpower.BACHELOR032A_PDF,
    hoverpower.BACHELOR032_PDF,
    hoverpower.BACHELOR037_PDF,
    hoverpower.BACHELOR039_PDF,
    hoverpower.BACHELOR041A_PDF,
    hoverpower.BACHELOR056_PDF,
    hoverpower.BACHELOR077_PDF,
    hoverpower.BACHELOR078_PDF,
    hoverpower.BACHELOR085_PDF,
    hoverpower.BACHELOR086_PDF,
    hoverpower.BACHELOR101_PDF,
    hoverpower.BACHELOR105_PDF,
    hoverpower.BACHELOR111_PDF,
    hoverpower.BACHELOR128_PDF,
    hoverpower.BOOK007_PDF,
    hoverpower.DISS143_PDF,
    hoverpower.DISS144_PDF,
    hoverpower.DISS148_PDF,
    hoverpower.DISS170B_PDF,
    hoverpower.DISS480_PDF,
    hoverpower.DOCU009_PDF,
    hoverpower.DOCU014_PDF,
    hoverpower.DOCU027_PDF,
    # hoverpower.HC_BACH106,
    # hoverpower.HC_DISS128,
    # hoverpower.HC_DISS148,
    # hoverpower.HC_DISS166,
    # hoverpower.HC_DISS171,
    # hoverpower.HC_DISS193,
    hoverpower.HOME007_PDF,
    hoverpower.HOME018_PDF,
    hoverpower.HOME020_PDF,
    hoverpower.HOME021B_PDF,
    hoverpower.HOME022_PDF,
    hoverpower.HOME022B_PDF,
    hoverpower.MASTER049_PDF,
    hoverpower.MASTER072_PDF,
    hoverpower.MASTER075_PDF,
    hoverpower.MASTER089_PDF,
    hoverpower.MASTER091A_PDF,
    hoverpower.MASTER091B_PDF,
    hoverpower.MASTER099C_PDF,
    hoverpower.MASTER110_PDF,
    hoverpower.MASTER127_PDF,
    hoverpower.MASTER155_PDF,
    hoverpower.MASTER193_PDF,
    hoverpower.PAPER14B_PDF,
    hoverpower.PAPER18_PDF,
    hoverpower.TECH019_PDF,
    hoverpower.TECH024_PDF,
]

WORKER = utilotest.worker_count(7, onci=len(RESOURCES))


def pytest_sessionstart(session):  # pylint:disable=W0613
    hoverpower.run()


RAWMAKER = '--text --line --horizontals ' + gennex.CONFIG


def extract(resources):
    gennex.extract(
        resources,
        rawmaker=RAWMAKER,
        oneline=None,
        pagenumber=True,
        cleanup=True,
        worker=WORKER,
    )


RESOURCES_NOTITLE = [
    hoverpower.DOCU027_PDF,
]


def extract_notitle(resources):
    gennex.extract_removepages(
        resources,
        removepages='0',
        folder='notitle',
        pages='0:10',
        pagenumber=True,
        cleanup=True,
        rawmaker=RAWMAKER,
        oneline=None,
        worker=1,
    )
