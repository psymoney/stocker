import json
import xmltodict
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(BASE_DIR + "/CORPCODE.xml", 'r', encoding='utf-8') as f:
    xmlString = f.read()

jsonString = json.dumps(xmltodict.parse(xmlString),
                        ensure_ascii=False, indent=4)


with open(BASE_DIR + "/corpcode.json", "w", encoding='utf-8') as f:
    f.write(jsonString)
