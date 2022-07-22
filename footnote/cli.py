#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila

import footnote

DESCRIPTION = 'TODO'

WORKPLAN = [
    utila.create_step(
        'plain',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='text_text'),
            utila.ResultFile(producer='rawmaker', name='text_positions'),
            utila.ResultFile(producer='rawmaker', name='fonts_header'),
            utila.ResultFile(producer='rawmaker', name='fonts_content'),
            utila.ResultFile('rawmaker', name='horizontals_horizontals'),
        ],
        output=('plain',),
    ),
    utila.create_step(
        'highnote',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='text_text'),
            utila.ResultFile(producer='rawmaker', name='text_positions'),
            utila.ResultFile(producer='rawmaker', name='fonts_header'),
            utila.ResultFile(producer='rawmaker', name='fonts_content'),
            utila.ResultFile('rawmaker', name='horizontals_horizontals'),
        ],
        output=('highnote',),
    ),
    utila.create_step(
        'result',
        inputs=[
            utila.ResultFile(producer='footnote', name='highnote_highnote'),
            utila.ResultFile(producer='footnote', name='plain_plain'),
        ],
        output=('result',),
    ),
    utila.create_step(
        'legacy',
        inputs=[
            utila.ResultFile(producer='footnote', name='result_result'),
        ],
        output=('legacy',),
    ),
]


def rename(path):
    if not isinstance(path, str):
        path = [rename(item) for item in path]
        return path
    path = utila.rreplace(
        path,
        pattern='footnote_legacy_legacy',
        replace='groupme__footer_footerheader',
    )
    return path


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=footnote.ROOT,
        featurepackage='footnote.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=footnote.PROCESS,
            pages=True,
            rename=rename,
            version=footnote.__version__,
        ),
    )
