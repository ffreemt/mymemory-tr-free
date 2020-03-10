''' sanity check
'''
# import pytest

from mymemory_tr import MymemoryTr


def test_sanity():
    ''' sanity check '''
    translate = MymemoryTr().translate
    del translate
    assert 1
