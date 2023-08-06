# pupil-pthreads-win

This is a precompiled version of pthreads for windows wrapped in a python package.
We use it as dependency for various modules for the pupil core software.

This wrapper contains a x64 precompiled version of pthreads-win 2.9.1 from https://sourceware.org/pthreads-win32/ from Ross Johnson.
The original licensing information can be found in [COPYING](src/pupil_pthreads_win/data/COPYING) and [COPYING.LIB](src/pupil_pthreads_win/data/COPYING.LIB).

## Installation

Note that this library only provides pthreads for windows and thus you are not recommended to use it  on another operating system. When trying to use it on another operating system, you might receive a warning.

Install from PyPI:
```bash
pip install pupil-pthreads-win
```
