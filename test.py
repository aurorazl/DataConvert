import time
import pyprind
import mmcv
from label_tool import annotations_to_voc_xml_file

a = {"1":"a","3":"c","2":"b"}
print(sorted(a.items(),key=lambda x:x[0]))
