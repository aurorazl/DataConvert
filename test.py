import time
import pyprind
import mmcv
from label_tool import annotations_to_voc_xml_file

annotations_to_voc_xml_file([("person",1,2,3,4)],120,235,"./images/test.xml",True)
