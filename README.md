# memory-tr-free ![Python3.6|3.7 package](https://github.com/ffreemt/mymemory-tr-free/workflows/Python3.6%7C3.7%20package/badge.svg)[![codecov](https://codecov.io/gh/ffreemt/memory-tr-free/branch/master/graph/badge.svg)](https://codecov.io/gh/ffreemt/memory-tr-free)
translate for free with async and proxy support

### Installation
Not available yet
```pip install memory-tr-free```

Validate installation
```
python -c "import mymemory_tr; print(mymemory_tr.__version__)"
0.0.1
```

### Usage

```
import asyncio
from mymemory_tr import mymemory_tr

asyncio.get_event_loop().run_until_complete(mymemory_tr('test this and that'))
# '测试这个和那个'
```

### Acknowledgments

* Thanks to everyone whose code was used
