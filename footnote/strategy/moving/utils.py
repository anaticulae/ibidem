# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def isendnote(numbers: list) -> False:
    """\
    >>> isendnote([1, 1, 1, 2])
    True
    """
    # TODO: VERY SIMPLE APPROACH
    small, high = utila.partition(
        key=lambda x: x <= 2,
        items=numbers,
    )
    if len(small) > len(high):
        return True
    return False


def footnote_numbers_flat(footers: list) -> list:
    numbers = []
    for footer in footers:
        for note in footer.footer.notes:
            if note.number is None:
                continue
            if not isinstance(note.number, int):
                utila.log(f'invalid footenumber: {note.number}')
                continue
            numbers.append(note.number)
    return numbers
