from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .models import Corporation
from .modules import Report, FinancialReport
import psycopg2
import requests
import json


class CompanyLookupView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        lookup_value = request.query_params["lookupValue"]
        consolidation = request.query_params["consolidation"]

        report = FinancialReport()
        corporate_code = report.get_corporate_code(lookup_value)

        if str(corporate_code) == 'Corporation matching query does not exist.':
            return Response(data={"message": str(corporate_code)}, status=status.HTTP_404_NOT_FOUND)
        else:
            financial_statements = report.get_financial_statements(
                corporate_code, consolidation_key)
            financial_reports = report.get_financial_reports(
                financial_statements)

        return Response(data={"reports: ": financial_reports}, status=status.HTTP_200_OK)
