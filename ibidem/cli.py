#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utilo

import ibidem

DESCRIPTION = 'TODO'

WORKPLAN = [
    utilo.create_step(
        'plain',
        inputs=[
            utilo.ResultFile(producer='rawmaker', name='text_text'),
            utilo.ResultFile(producer='rawmaker', name='text_positions'),
            utilo.ResultFile('rawmaker', name='horizontals_horizontals'),
        ],
        output=('plain',),
    ),
    utilo.create_step(
        'highnote',
        inputs=[
            utilo.ResultFile(producer='rawmaker', name='text_text'),
            utilo.ResultFile(producer='rawmaker', name='text_positions'),
            utilo.ResultFile('rawmaker', name='horizontals_horizontals'),
        ],
        output=('highnote',),
    ),
    utilo.create_step(
        'result',
        inputs=[
            utilo.ResultFile(producer='footnote', name='highnote_highnote'),
            utilo.ResultFile(producer='footnote', name='plain_plain'),
        ],
        output=('result',),
    ),
    utilo.create_step(
        'legacy',
        inputs=[
            utilo.ResultFile(producer='footnote', name='result_result'),
        ],
        output=('legacy',),
    ),
]


def rename(path):
    if not isinstance(path, str):
        path = [rename(item) for item in path]
        return path
    path = utilo.rreplace(
        path,
        pattern='footnote__legacy_legacy',
        replace='groupme__footer_footerheader',
    )
    return path


def main():
    utilo.featurepack(
        workplan=WORKPLAN,
        root=ibidem.ROOT,
        featurepackage='ibidem.feature',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=ibidem.PROCESS,
            pages=True,
            rename=rename,
            version=ibidem.__version__,
        ),
    )
