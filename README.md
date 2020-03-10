# mymemory-tr-free ![Python3.6|3.7 package](https://github.com/ffreemt/mymemory-tr-free/workflows/Python3.6%7C3.7%20package/badge.svg)[![codecov](https://codecov.io/gh/ffreemt/memory-tr-free/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/memory-tr-free)[![PyPI version](https://badge.fury.io/py/mymemory-tr-free.svg)](https://badge.fury.io/py/mymemory-tr-free)
translate for free with proxy support

Daily quota: 10000 chars for a single IP; use a proxy to another 10000 

### Installation
```pip install mymemory-tr-free```

Validate installation
```
python -c "import mymemory_tr; print(mymemory_tr.__version__)"
0.0.1
```

### Usage

```
from mymemory_tr import MymemoryTr

mymemory_tr = MymemoryTr().translate

mymemory_tr('test this and that'))
# '测试这个和那个'

# use a proxy per instance
proxy = 'http://127.0.0.1:8888'
mymemory_tr = MymemoryTr(proxy=proxy).translate
mymemory_tr('test this and that')

# use a proxy per request
mymemory_tr = MymemoryTr().translate
proxy = 'http://127.0.0.1:8888'
mymemory_tr('test this and that', proxy=proxy)

# source and destination can be identifid by RFC3066 (ISO 639-1)
mymemory_tr = MymemoryTr(to_lang='de').translate
mymemory_tr('Test this and that and more')
# 'Testen Sie dieses und das und mehr'

```

### Acknowledgments

* Thanks to everyone whose code was used
