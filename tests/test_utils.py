# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilotest

import ibidem.layout
import ibidem.parser.highnote


@utilotest.longrun
def test_footnote_highnotes_split(master72page14):
    footer = master72page14
    splitted = list(ibidem.layout.split_textinfo(footer))
    assert splitted, splitted
    assert len(splitted) == 7, splitted


@utilotest.longrun
def test_footnote_highnotes_split_mixed_in_text(master89page7):
    """Test to extract only starting highnotes.

    In this example, there is a highnote inside the text flow.
    """
    footer = master89page7
    splitted = list(ibidem.layout.split_textinfo(footer))
    assert splitted, splitted
    assert len(splitted) == 2, splitted
    merged = ibidem.layout.merge_online(splitted)
    assert len(merged) == 1, merged


@utilotest.longrun
def test_footnote_highnotes_split_mixed_in_text_tripple(master89page19):
    """Test to extract only starting highnotes.

    In this example, there is a highnote inside the text flow and after
    this there are two more footnotes.
    """
    footer = master89page19
    footer = ibidem.parser.highnote.append_newline(footer)
    splitted = list(ibidem.layout.split_textinfo(footer))
    assert splitted, splitted
    assert len(splitted) == 4, splitted
    merged = ibidem.layout.merge_online(splitted)
    assert len(merged) == 3, merged

    thirdnote_text = merged[2][1].text
    thirdnote_text = thirdnote_text.strip()  # TODO: REMOVE LATER
    expected = ('Das Schema fasst Vogler (vgl. 21998: 74f.) wie folgt zusammen:'
                ' Der Held wird in seinem Leben in der\ngewohnten Welt '
                'vorgestellt und erh')
    assert thirdnote_text.startswith(expected), thirdnote_text
