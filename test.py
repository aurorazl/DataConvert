import time
import pyprind
import mmcv

import mmcv

tasks = list(range(10))

# for task in mmcv.track_iter_progress(tasks):
#     time.sleep(1)
#     print(task)
import pyprind
# pbar = pyprind.ProgBar(10,monitor=True)
# for i in range(10):
#     time.sleep(0.3)
#     pbar.update()
for i, task in enumerate(mmcv.track_iter_progress(tasks)):
    # do something like print
    time.sleep(0.3)
    print(i)
    print(task)
