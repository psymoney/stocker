from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
import requests
import json


class Report:
    def __init__(self, report_type,
                 account_name,
                 current_period,
                 current_period_amount,
                 prior_period,
                 prior_period_amount,
                 past_prior_period,
                 past_prior_period_amount):
        self.reportType = report_type
        self.accountName = account_name
        self.currentPeriod = current_period
        self.currentPeriodAmount = current_period_amount
        self.priorPeriod = prior_period
        self.priorPeriodAmount = prior_period_amount
        self.pastPriorPeriod = past_prior_period
        self.pastPriorPeriodAmount = past_prior_period_amount

    def __str__(self):
        return 'report type = {} account name = {} current period amount = {} prior period amount = {} past prior period amount = {}'.format(
            self.reportType, self.accountName, self.currentPeriodAmount, self.priorPeriodAmount, self.pastPriorPeriodAmount)

    def to_JSON_response(self):
        return {
            "reportType": self.reportType,
            "accountName": self.accountName,
            "currentPeriod": self.currentPeriod,
            "currentPeriodAmount": self.currentPeriodAmount,
            "priorPeriod": self.priorPeriod,
            "priorPeriodAmount": self.priorPeriodAmount,
            "pastPriorPeriod": self.pastPriorPeriod,
            "pastPriorPeriodAmount": self.pastPriorPeriodAmount
        }


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

        # TODO(SY): improve method
        def get_financial_report(financials):
            financial_reports = []

            for report in financials['list']:
                account_name = report['account_nm']
                if account_name in set(["수익(매출액)", "수익", "매출액", "매출총액"]):
                    revenue = Report(report['sj_nm'], report['account_nm'], report['thstrm_nm'], report['thstrm_amount'],
                                     report['frmtrm_nm'], report['frmtrm_amount'], report['bfefrmtrm_nm'], report['bfefrmtrm_amount'])
                    current_year_growth = float(report['thstrm_amount']) / \
                        float(report['frmtrm_amount']) - 1
                    prior_year_growth = float(report['frmtrm_amount']) / \
                        float(report['bfefrmtrm_amount']) - 1
                    revenue_growth = Report(report['sj_nm'], "매출성장률", report['thstrm_nm'], current_year_growth,
                                            report['frmtrm_nm'], prior_year_growth, report['bfefrmtrm_nm'], '-')
                    financial_reports.append(revenue_growth.to_JSON_response())
                elif account_name in set(["매출총이익", "매출총수익", "매출총익"]):
                    gross_profit = Report(report['sj_nm'], report['account_nm'], report['thstrm_nm'], report['thstrm_amount'],
                                          report['frmtrm_nm'], report['frmtrm_amount'], report['bfefrmtrm_nm'], report['bfefrmtrm_amount'])
                    financial_reports.append(gross_profit.to_JSON_response())
                elif account_name in set(["영업이익(손실)", "영업이익"]):
                    operating_profit = Report(report['sj_nm'], report['account_nm'], report['thstrm_nm'], report['thstrm_amount'],
                                              report['frmtrm_nm'], report['frmtrm_amount'], report['bfefrmtrm_nm'], report['bfefrmtrm_amount'])
                    financial_reports.append(
                        operating_profit.to_JSON_response())
                elif account_name in set(["당기순이익(손실)", "당기순이익"]) and report['sj_nm'] == "손익계산서":
                    net_income = Report(report['sj_nm'], report['account_nm'], report['thstrm_nm'], report['thstrm_amount'],
                                        report['frmtrm_nm'], report['frmtrm_amount'], report['bfefrmtrm_nm'], report['bfefrmtrm_amount'])
                    financial_reports.append(net_income.to_JSON_response())
                elif account_name == "자본총계" and report['sj_nm'] == "재무상태표":
                    total_equity = Report(report['sj_nm'], report['account_nm'], report['thstrm_nm'], report['thstrm_amount'],
                                          report['frmtrm_nm'], report['frmtrm_amount'], report['bfefrmtrm_nm'], report['bfefrmtrm_amount'])
                    financial_reports.append(total_equity.to_JSON_response())

            return financial_reports

        corporate_name = request.query_params["corporateName"]
        consolidation_key = request.query_params["consolidationKey"]
        if consolidation_key == "True":
            consolidation_key = "CFS"
        else:
            consolidation_key = "OFS"

        corporate_code = get_corporate_code(corporate_name)
        financials = get_financials()
        financial_reports = get_financial_report(financials)

        # TODO(SY): fix Response after implementing get method
        return Response(data={"reports": financial_reports}, status=status.HTTP_200_OK)
