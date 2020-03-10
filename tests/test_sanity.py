''' sanity check
'''
import pytest

from mymemory_tr import mymemory_tr


@pytest.mark.asyncio
async def test_sanity():
    ''' sanity check '''
    await mymemory_tr()
    assert 1
