from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
import requests
import json


class CompanyLookupView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):

        # TODO(SY): implement get_corporate_code method
        def get_corporate_code(name):
            return "00126380"

        def get_financials():
            URI = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json"
            API_KEY = "d3f02b844b4afaa11b10e188bc7a092fc1a63f25"
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

        # TODO(SY): implement get_process_financials method
        def get_process_financials(financials):
            financial_data = []
            for i in range(len(financials['list'])):
                if financials['list'][i]['sj_nm'] == "자본변동표":
                    continue

                data_list = {}
                data_list['report_type'] = financials['list'][i]['sj_nm']
                data_list['account_name'] = financials['list'][i]['account_nm']
                data_list['current_period'] = financials['list'][i]['thstrm_nm']
                data_list['current_period_amount'] = financials['list'][i]['thstrm_amount']
                data_list['prior_period'] = financials['list'][i]['frmtrm_nm']
                data_list['prior_period_amount'] = financials['list'][i]['frmtrm_amount']
                data_list['past_prior_period'] = financials['list'][i]['bfefrmtrm_nm']
                data_list['past_prior_period_amount'] = financials['list'][i]['bfefrmtrm_amount']
                financial_data.append(data_list)

            return financial_data

        def get_financial_report(financials):
            financial_report = []
            revenue_data = {}
            gross_profit_data = {}
            operating_profit_data = {}
            net_income_data = {}
            equity_data = {}

            # processing data for financial report
            for i in range(len(financials['list'])):
                if financials['list'][i]['account_nm'] == "수익(매출액)":
                    data_list = {}
                    revenue_data = financials['list'][i]

                    # Add revenue growth to report
                    data_list['reportType'] = financials['list'][i]['sj_nm']
                    data_list['accountName'] = "매출성장률"
                    data_list['currentPeriod'] = financials['list'][i]['thstrm_nm']
                    data_list['currentPeriodAmount'] = (
                        float(financials['list'][i]['thstrm_amount']) / float(financials['list'][i]['frmtrm_amount'])) - 1
                    data_list['priorPeriod'] = financials['list'][i]['frmtrm_nm']
                    data_list['priorPeriodAmount'] = (
                        float(financials['list'][i]['frmtrm_amount']) / float(financials['list'][i]['bfefrmtrm_amount'])) - 1
                    data_list['pastPriorPeriod'] = financials['list'][i]['bfefrmtrm_nm']
                    data_list['pastPriorPeriodAmount'] = '-'
                    financial_report.append(data_list)

                if financials['list'][i]['account_nm'] == "매출총이익":
                    data_list = {}
                    gross_profit_data = financials['list'][i]

                    # Add gross profit margin to report
                    data_list['reportType'] = financials['list'][i]['sj_nm']
                    data_list['accountName'] = "매출총이익률"
                    data_list['currentPeriod'] = financials['list'][i]['thstrm_nm']
                    data_list['currentPeriodAmount'] = (
                        float(financials['list'][i]['thstrm_amount']) / float(revenue_data['thstrm_amount']))
                    data_list['priorPeriod'] = financials['list'][i]['frmtrm_nm']
                    data_list['priorPeriodAmount'] = (
                        float(financials['list'][i]['frmtrm_amount']) / float(revenue_data['frmtrm_amount']))
                    data_list['pastPriorPeriod'] = financials['list'][i]['bfefrmtrm_nm']
                    data_list['pastPriorPeriodAmount'] = (
                        float(financials['list'][i]['bfefrmtrm_amount']) / float(revenue_data['bfefrmtrm_amount']))
                    financial_report.append(data_list)

                if financials['list'][i]['account_nm'] == "영업이익(손실)":
                    data_list = {}

                    # Add operating profit margin to report
                    data_list['reportType'] = financials['list'][i]['sj_nm']
                    data_list['accountName'] = "영업이익률"
                    data_list['currentPeriod'] = financials['list'][i]['thstrm_nm']
                    data_list['currentPeriodAmount'] = (
                        float(financials['list'][i]['thstrm_amount']) / float(revenue_data['thstrm_amount']))
                    data_list['priorPeriod'] = financials['list'][i]['frmtrm_nm']
                    data_list['priorPeriodAmount'] = (
                        float(financials['list'][i]['frmtrm_amount']) / float(revenue_data['frmtrm_amount']))
                    data_list['pastPriorPeriod'] = financials['list'][i]['bfefrmtrm_nm']
                    data_list['pastPriorPeriodAmount'] = (
                        float(financials['list'][i]['bfefrmtrm_amount']) / float(revenue_data['bfefrmtrm_amount']))
                    financial_report.append(data_list)

                if financials['list'][i]['account_nm'] == "당기순이익(손실)" and financials['list'][i]['sj_nm'] == "손익계산서":
                    data_list = {}
                    net_income_data = financials['list'][i]

                    # Add net income margin to report
                    data_list['reportType'] = financials['list'][i]['sj_nm']
                    data_list['accountName'] = "당기순이익률"
                    data_list['currentPeriod'] = financials['list'][i]['thstrm_nm']
                    data_list['currentPeriodAmount'] = (
                        float(financials['list'][i]['thstrm_amount']) / float(revenue_data['thstrm_amount']))
                    data_list['priorPeriod'] = financials['list'][i]['frmtrm_nm']
                    data_list['priorPeriodAmount'] = (
                        float(financials['list'][i]['frmtrm_amount']) / float(revenue_data['frmtrm_amount']))
                    data_list['pastPriorPeriod'] = financials['list'][i]['bfefrmtrm_nm']
                    data_list['pastPriorPeriodAmount'] = (
                        float(financials['list'][i]['bfefrmtrm_amount']) / float(revenue_data['bfefrmtrm_amount']))
                    financial_report.append(data_list)

                if financials['list'][i]['account_nm'] == "자본총계" and financials['list'][i]['sj_nm'] == "재무상태표":
                    data_list = {}
                    equity_data = financials['list'][i]

            if revenue_data:
                data_list = {}
                # Add revenue to report
                data_list['reportType'] = revenue_data['sj_nm']
                data_list['accountName'] = revenue_data['account_nm']
                data_list['currentPeriod'] = revenue_data['thstrm_nm']
                data_list['currentPeriodAmount'] = revenue_data['thstrm_amount']
                data_list['priorPeriod'] = revenue_data['frmtrm_nm']
                data_list['priorPeriodAmount'] = revenue_data['frmtrm_amount']
                data_list['pastPriorPeriod'] = revenue_data['bfefrmtrm_nm']
                data_list['pastPriorPeriodAmount'] = revenue_data['bfefrmtrm_amount']
                financial_report.append(data_list)

            if gross_profit_data:
                data_list = {}
                # Add gross profit to report
                data_list['reportType'] = gross_profit_data['sj_nm']
                data_list['accountName'] = gross_profit_data['account_nm']
                data_list['currentPeriod'] = gross_profit_data['thstrm_nm']
                data_list['currentPeriodAmount'] = gross_profit_data['thstrm_amount']
                data_list['priorPeriod'] = gross_profit_data['frmtrm_nm']
                data_list['priorPeriodAmount'] = gross_profit_data['frmtrm_amount']
                data_list['pastPriorPeriod'] = gross_profit_data['bfefrmtrm_nm']
                data_list['pastPriorPeriodAmount'] = gross_profit_data['bfefrmtrm_amount']
                financial_report.append(data_list)

            if operating_profit_data:
                # Add operating profit to report
                data_list['reportType'] = operating_profit_data['sj_nm']
                data_list['accountName'] = operating_profit_data['account_nm']
                data_list['currentPeriod'] = operating_profit_data['thstrm_nm']
                data_list['currentPeriodAmount'] = operating_profit_data['thstrm_amount']
                data_list['priorPeriod'] = operating_profit_data['frmtrm_nm']
                data_list['priorPeriodAmount'] = operating_profit_data['frmtrm_amount']
                data_list['pastPriorPeriod'] = operating_profit_data['bfefrmtrm_nm']
                data_list['pastPriorPeriodAmount'] = operating_profit_data['bfefrmtrm_amount']
                financial_report.append(data_list)

            if net_income_data:
                data_list = {}
                # Add net income to report
                data_list['reportType'] = net_income_data['sj_nm']
                data_list['accountName'] = net_income_data['account_nm']
                data_list['currentPeriod'] = net_income_data['thstrm_nm']
                data_list['currentPeriodAmount'] = net_income_data['thstrm_amount']
                data_list['priorPeriod'] = net_income_data['frmtrm_nm']
                data_list['priorPeriodAmount'] = net_income_data['frmtrm_amount']
                data_list['pastPriorPeriod'] = net_income_data['bfefrmtrm_nm']
                data_list['pastPriorPeriodAmount'] = net_income_data['bfefrmtrm_amount']
                financial_report.append(data_list)

            if equity_data:
                # Add equity to report
                data_list['reportType'] = equity_data['sj_nm']
                data_list['accountName'] = equity_data['account_nm']
                data_list['currentPeriod'] = equity_data['thstrm_nm']
                data_list['currentPeriodAmount'] = equity_data['thstrm_amount']
                data_list['priorPeriod'] = equity_data['frmtrm_nm']
                data_list['priorPeriodAmount'] = equity_data['frmtrm_amount']
                data_list['pastPriorPeriod'] = equity_data['bfefrmtrm_nm']
                data_list['pastPriorPeriodAmount'] = equity_data['bfefrmtrm_amount']
                financial_report.append(data_list)

            if net_income_data and equity_data:
                # Add ROE to report
                data_list['reportType'] = equity_data['sj_nm']
                data_list['accountName'] = "ROE"
                data_list['currentPeriod'] = equity_data['thstrm_nm']
                data_list['currentPeriodAmount'] = (
                    float(net_income_data['thstrm_amount']) / float(equity_data['thstrm_amount']))
                data_list['priorPeriod'] = equity_data['frmtrm_nm']
                data_list['priorPeriodAmount'] = (
                    float(net_income_data['frmtrm_amount']) / float(equity_data['frmtrm_amount']))
                data_list['pastPriorPeriod'] = equity_data['bfefrmtrm_nm']
                data_list['pastPriorPeriodAmount'] = (
                    float(net_income_data['bfefrmtrm_amount']) / float(equity_data['bfefrmtrm_amount']))
                financial_report.append(data_list)

            return financial_report

        corporate_name = request.query_params["corporateName"]
        consolidation_key = request.query_params["consolidationKey"]
        if consolidation_key == "True":
            consolidation_key = "CFS"
        else:
            consolidation_key = "OFS"

        # TODO(SY): delete below print code after test
        print(
            f"corporate_name = {corporate_name} \nconsolidation_key = {consolidation_key}")

        corporate_code = get_corporate_code(corporate_name)
        financials = get_financials()
        financial_data = get_process_financials(financials)
        financial_report = get_financial_report(financials)
        print(financial_report)  # uncommnet after test

        # TODO(SY): fix Response after implementing get method
        return Response(data={"corporate_name": corporate_name, "consolidation_key": consolidation_key}, status=status.HTTP_200_OK)
