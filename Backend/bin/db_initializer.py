import json
import os.path


def Initilize_Db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    f = open(BASE_DIR + '/corpcode.json', 'r', encoding='utf-8')
    corporations = json.load(f)
    corporations = corporations['result']['list']
    corps = []
    for corp in corporations[:10]:
        # print(type(corp['corp_code']), type(corp['corp_name']),type(corp['stock_code']) )
        if type(corp['corp_code']) != int:
            continue
        if type(corp['corp_name']) != str:
            continue
        if type(corp['stock_code']) != str:
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
