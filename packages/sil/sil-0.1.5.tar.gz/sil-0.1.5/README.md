# SIL
SIL (Status In-Line) is a simple progress bar that provides sufficient
flexibility and compatibility with the `multiprocessing` library.

# Basic Usage
```python
from sil import Sil

status = Sil(
    total=200,     # what is the number you are counting to
    length=40,     # how many characters should be use to print the progress bar
    every=10,      # after how many elements should the progress bar update (e.g. throttling)
    indicator='*' # what character should be used in the progress bar
)

for i, el in elements:
    status.tick()

```

# Multiprocessing example
It can be useful to see the progress of you code when parallelized
```python
from sil import Sil
from multiprocessing import Pool, Value

# global shared memory counter
_i = Value('i', -1, lock=True)

def mp_tick(i, status):
    # do something for current element in parallel

    with _i.get_lock():
        _i.value += 1

    status.update(_i.value)

with Pool(processes=4) as pool:
    pool.starmap(mp_tick, [(i, status) for i in range(200)])

```
