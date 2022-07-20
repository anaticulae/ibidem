# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

import footnote
# pylint:disable=W0611
from tests.fixtures import bachelor111page10
from tests.fixtures import master72page14
from tests.fixtures import master89page7
from tests.fixtures import master89page19
from tests.fixtures import navigator

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = footnote.PROCESS

RESOURCES = [
    (power.BACHELOR051_PDF, '0:25'),
    (power.BACHELOR063_PDF, '0:20'),
    (power.BACHELOR076_PDF, '0:25'),
    (power.BACHELOR090_PDF, '0:25'),
    (power.BACHELOR241_PDF, '0:100'),
    (power.BOOK173_PDF, '0:100'),
    (power.DISS178_PDF, '0:30'),
    (power.DISS218_PDF, '0:100'),
    (power.DISS264_PDF, '0:50'),
    (power.DISS273_PDF, '30:60'),
    (power.DISS287_PDF, '0:100'),
    (power.DISS406_PDF, '0:75,100:150'),
    (power.MASTER098_PDF, '0:15'),
    (power.MASTER099_PDF, '0:30'),
    (power.MASTER112_PDF, '5,6'),
    (power.MASTER116_PDF, '50:117'),
    (power.ORDER009_PDF, '0:10'),
    genex.todo(
        power.DISS172_PDF,
        figureo=True,
        tablero=True,
        rawmaker=genex.CONFIG,
    ),
    genex.todo(power.DOCU007_PDF, tablero=True, rawmaker=genex.CONFIG),
    genex.todo(power.MASTER063_PDF, figureo=True),
    power.BACHELOR028_PDF,
    power.BACHELOR032A_PDF,
    power.BACHELOR032_PDF,
    power.BACHELOR037_PDF,
    power.BACHELOR039_PDF,
    power.BACHELOR041A_PDF,
    power.BACHELOR056_PDF,
    power.BACHELOR077_PDF,
    power.BACHELOR078_PDF,
    power.BACHELOR085_PDF,
    power.BACHELOR086_PDF,
    power.BACHELOR101_PDF,
    power.BACHELOR105_PDF,
    power.BACHELOR111_PDF,
    power.BACHELOR128_PDF,
    power.BOOK007_PDF,
    power.DISS143_PDF,
    power.DISS144_PDF,
    power.DISS148_PDF,
    power.DISS170B_PDF,
    power.DISS480_PDF,
    power.DOCU009_PDF,
    power.DOCU014_PDF,
    power.DOCU027_PDF,
    power.HC_BACH106,
    power.HC_DISS128,
    power.HC_DISS148,
    power.HC_DISS166,
    power.HC_DISS171,
    power.HC_DISS193,
    power.HOME018_PDF,
    power.MASTER049_PDF,
    power.MASTER072_PDF,
    power.MASTER075_PDF,
    power.MASTER089_PDF,
    power.MASTER091A_PDF,
    power.MASTER091B_PDF,
    power.MASTER099C_PDF,
    power.MASTER110_PDF,
    power.MASTER127_PDF,
    power.MASTER155_PDF,
    power.MASTER193_PDF,
    power.PAPER14B_PDF,
    power.PAPER18_PDF,
    power.TECH019_PDF,
    power.TECH024_PDF,
]

WORKER = 5


def pytest_sessionstart(session):  # pylint:disable=W0613
    power.run()


RAWMAKER = '--text --fonts --border --line --horizontals ' + genex.CONFIG


def extract(resources):
    genex.extract(
        resources,
        rawmaker=RAWMAKER,
        oneline=None,
        pagenumber=True,
        cleanup=True,
        worker=WORKER,
    )


RESOURCES_NOTITLE = [
    power.DOCU027_PDF,
]


def extract_notitle(resources):
    genex.extract_removepages(
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
