''' dummy test '''
from mymemory_tr import __version__, MymemoryTr


def test_version():
    ''' test versioin '''
    assert __version__ == '0.0.1'


def test_instance_de():
    ''' test_instance_de '''
    mymemory_tr = MymemoryTr(to_lang='de').translate
    res = mymemory_tr('Test this and that and more')
    _ = ['testen', 'sie', 'und', 'das', 'mehr']
    assert all(map(lambda elm: elm in res.lower(), _))


def test_request_de():
    ''' test_request_de '''
    mymemory_tr = MymemoryTr(to_lang='fr').translate
    res = mymemory_tr('Test this and that and more', to_lang='de')
    # assert not res
    _ = ['testen', 'sie', 'und', 'das', 'mehr']
    assert all(map(lambda elm: elm in res.lower(), _[0]))


def test_instance_fr():
    ''' test_instance_fr '''
    mymemory_tr = MymemoryTr(to_lang='fr').translate
    res = mymemory_tr('Test this and that and more', to_lang='fr')
    # assert not res
    _ = ['testez', 'ceci', 'et', 'encore']
    assert all(map(lambda elm: elm in res.lower(), _))


def test_request_fr():
    ''' test_request_fr '''
    mymemory_tr = MymemoryTr(to_lang='de').translate
    res = mymemory_tr('Test this and that and more', to_lang='fr')
    _ = ['testen', 'sie', 'und' 'das', 'mehr']
    _ = ['testez', 'ceci', 'et', 'encore']
    assert all(map(lambda elm: elm in res.lower(), _))
