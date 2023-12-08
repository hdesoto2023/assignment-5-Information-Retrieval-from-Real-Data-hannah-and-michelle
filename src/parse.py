import json
import sys

from xml.etree.ElementTree import iterparse

for _, elem in iterparse(sys.argv[1]):
    if elem.tag == "Record":
        print(json.dumps(elem.attrib))
