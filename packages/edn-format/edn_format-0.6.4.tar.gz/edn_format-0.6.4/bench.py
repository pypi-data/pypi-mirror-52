# -*- coding: UTF-8 -*-

import timeit

try:
    import cProfile as profile
except ImportError:
    import profile

from edn_format import loads

if False:
    loads, timeit, profile

with open("bench1.edn") as f:
    edn = f.read()

print(timeit.timeit('loads(edn)', globals=globals(), number=200))

# profile.runctx('for _ in range(100): loads(edn)',
#         globals=globals(), locals=locals())

# 2079966 function calls (2061017 primitive calls) in 1.963 seconds
