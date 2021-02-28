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
        search_key = request.query_params["searchKey"]
        consolidation_key = request.query_params["consolidationKey"]
        if consolidation_key == "True":
            consolidation_key = "CFS"
        else:
            consolidation_key = "OFS"

        corporate_code = FinancialReport.get_corporate_code(search_key)
        if(corporate_code == "error"):
            return Response(data={"error: doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            financial_statements = FinancialReport.get_financial_statements(
                corporate_code, consolidation_key)
            financial_reports = FinancialReport.get_financial_reports(
                financial_statements)

        return Response(data={"reports: ": financial_reports}, status=status.HTTP_200_OK)
