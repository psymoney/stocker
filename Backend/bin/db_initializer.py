import json
import os.path


def Initilize_Db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    f = open(BASE_DIR + '\corpcode.json', 'r', encoding='utf-8')
    corporations = json.load(f)
    corporations = corporations['result']['list']
    print(corporations[0])
    corps = []
    for corp in corporations:
        temp = {
            "model": "financials.corporation",
            "fields": {
                "code": corp['corp_code'],
                "name": corp['corp_name'],
                "ticker": corp['stock_code']
            }
        }

        corps.append(temp)

    print(corps[0])
    with open(BASE_DIR + "\corp.json", "w") as json_file:
        json.dump(corps, json_file)


Initilize_Db()
