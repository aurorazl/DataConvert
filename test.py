import time
import pyprind
li = list(range(10))
wait=li.copy()
for i in li:
    if i>5:
        wait.remove(i)
print(li)
print(wait)
