from .models import Corporation
import psycopg2
import requests
import json
from django.db import models


class Report:
    def __init__(self, report_type,
                 account_name,
                 current_period,
                 current_period_amount,
                 prior_period,
                 prior_period_amount,
                 past_prior_period,
                 past_prior_period_amount):
        self.report_type = report_type
        self.account_name = account_name
        self.current_period = current_period
        self.current_period_amount = current_period_amount
        self.prior_period = prior_period
        self.prior_period_amount = prior_period_amount
        self.past_prior_period = past_prior_period
        self.past_prior_period_amount = past_prior_period_amount

    def __str__(self):
        return 'report type = {} account name = {} current period amount = {} prior period amount = {} past prior period amount = {}'.format(
            self.report_type, self.account_name, self.current_period_amount, self.prior_period_amount, self.past_prior_period_amount)

    def to_JSON_response(self):
        return {
            "reportType": self.report_type,
            "accountName": self.account_name,
            "currentPeriod": self.current_period,
            "currentPeriodAmount": self.current_period_amount,
            "priorPeriod": self.prior_period,
            "priorPeriodAmount": self.prior_period_amount,
            "pastPriorPeriod": self.past_prior_period,
            "pastPriorPeriodAmount": self.past_prior_period_amount
        }


CorporateCodeNotFoundError = "corporate code not found"


class FinancialReport:
    def get_corporate_code(self, key):
        def search_by_name():
            try:
                search_result = Corporation.objects.get(name=str(key))
            except Corporation.DoesNotExist:
                return CorporateCodeNotFoundError
            else:
                return search_result.code

        def search_by_ticker():
            try:
                search_result = Corporation.objects.get(ticker=str(key))
            except Corporation.DoesNotExist:
                return CorporateCodeNotFoundError
            else:
                return search_result.code

        if key.isdigit():
            return search_by_ticker()
        else:
            return search_by_name()

    def get_financial_statements(self, corporate_code, consolidation_key):
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

    def get_financial_reports(self, financial_statements):
        financial_reports = []
        revenue = None
        gross_profit = None
        operating_profit = None
        net_income = None
        total_equity = None

        def get_report(financial_statements):
            report = Report(financial_statements['sj_nm'], financial_statements['account_nm'], financial_statements['thstrm_nm'], financial_statements['thstrm_amount'],
                            financial_statements['frmtrm_nm'], financial_statements['frmtrm_amount'], financial_statements['bfefrmtrm_nm'], financial_statements['bfefrmtrm_amount'])
            return report

        def get_growth_report(financial_statements, account_name):
            current_year_growth = str(float(financial_statements['thstrm_amount']) /
                                      float(financial_statements['frmtrm_amount']) - 1)
            prior_year_growth = str(float(financial_statements['frmtrm_amount']) /
                                    float(financial_statements['bfefrmtrm_amount']) - 1)
            report = Report(financial_statements['sj_nm'], account_name, financial_statements['thstrm_nm'], current_year_growth,
                            financial_statements['frmtrm_nm'], prior_year_growth, financial_statements['bfefrmtrm_nm'], '-')
            return report

        def get_ratio_report(numerator, denominator, account_name):
            current_period_value = str(float(
                numerator['thstrm_amount']) / float(denominator['thstrm_amount']))
            prior_period_value = str(float(
                numerator['frmtrm_amount']) / float(denominator['frmtrm_amount']))
            past_prior_period_value = str(float(
                numerator['bfefrmtrm_amount']) / float(denominator['bfefrmtrm_amount']))
            report = Report(numerator['sj_nm'], account_name, numerator['thstrm_nm'], current_period_value,
                            numerator['frmtrm_nm'], prior_period_value, numerator['bfefrmtrm_nm'], past_prior_period_value)
            return report

        for report in financial_statements['list']:
            account_name = report['account_nm']
            if account_name in set(["수익(매출액)", "수익", "매출액", "매출총액"]):
                revenue = get_report(report)
                financial_reports.append(revenue.to_JSON_response())
                revenue = report
                # Add revenue growth report
                revenue_growth = get_growth_report(report, "매출성장률")
                financial_reports.append(revenue_growth.to_JSON_response())
            elif account_name in set(["매출총이익", "매출총수익", "매출총익"]):
                gross_profit = get_report(report)
                financial_reports.append(gross_profit.to_JSON_response())
                gross_profit = report
            elif account_name in set(["영업이익(손실)", "영업이익"]):
                operating_profit = get_report(report)
                financial_reports.append(
                    operating_profit.to_JSON_response())
                operating_profit = report
            elif account_name in set(["당기순이익(손실)", "당기순이익"]) and report['sj_nm'] == "손익계산서":
                net_income = get_report(report)
                financial_reports.append(net_income.to_JSON_response())
                net_income = report
            elif account_name == "자본총계" and report['sj_nm'] == "재무상태표":
                total_equity = get_report(report)
                financial_reports.append(total_equity.to_JSON_response())
                total_equity = report

        # Add gross profit margin
        if gross_profit and revenue:
            gross_profit_margin = get_ratio_report(
                gross_profit, revenue, "매출총이익률")
            financial_reports.append(
                gross_profit_margin.to_JSON_response())
        # Add operating profit margin
        if operating_profit and revenue:
            operating_profit_margin = get_ratio_report(
                operating_profit, revenue, "영업이익률")
            financial_reports.append(
                operating_profit_margin.to_JSON_response())
        # Add net income margin
        if net_income and revenue:
            net_income_margin = get_ratio_report(
                net_income, revenue, "당기순이익률")
            financial_reports.append(net_income_margin.to_JSON_response())
        # Add ROE
        if net_income and total_equity:
            return_on_equity = get_ratio_report(
                net_income, total_equity, "ROE")
            financial_reports.append(return_on_equity.to_JSON_response())

        return financial_reports
