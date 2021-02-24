import json
import os.path


def Initilize_Db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    f = open(BASE_DIR + '/corpcode.json', 'r', encoding='utf-8')
    corporations = json.load(f)
    corporations = corporations['result']['list']
    corps = []
    for corp in corporations:
        if not corp:
            continue
        if (corp['stock_code']) == None:
            continue
        temp = {
            "model": "financials.corporation",
            "fields": {
                "code": corp['corp_code'],
                "name": corp['corp_name'],
                "ticker": corp['stock_code']
            }
        }

        corps.append(temp)
    with open(BASE_DIR + "/corp.json", "w", encoding='utf-8') as json_file:
        json_file.write(json.dumps(corps, ensure_ascii=False, indent=4))


Initilize_Db()
