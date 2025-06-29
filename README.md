Depends on:

* pillow
* python3
* perf

tested only on linux

**sobel_pure.py** is the bare program without external libraries

**sobel.py** has jpeg and dynamic thread setting support, depends on pillow and multiprocessing

**performance_full.sh** tests the performance of sobel.py

**performance_noext.sh** tests the performance of sobel_pure.py

both output to ./performance_logs

both have syntax like this:

```python3 sobel.py <input_file> <output_file> -t <threads>```
