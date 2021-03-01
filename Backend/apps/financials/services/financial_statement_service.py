import requests

URI = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json"
API_KEY = "d3f02b844b4afaa11b10e188bc7a092fc1a63f25"


class FinancialStatementService:
    def get_financial_statements(self, corporate_code, consolidation_key):
        business_year = 2019
        report_code = 11011

        # Request financial data from external API
        response = requests.get(URI, params={
            'crtfc_key': API_KEY,
            'corp_code': corporate_code,
            'bsns_year': business_year,
            'reprt_code': report_code,
            'fs_div': consolidation_key})

        return response.json()
