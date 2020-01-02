import time
import pyprind
import mmcv
# from label_tool import annotations_to_voc_xml_file
li=[]
with open("val.txt","r") as f:
    for i in f:
        li.append(i.strip())
    print("done",li)
