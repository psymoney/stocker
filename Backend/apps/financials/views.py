from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .modules import *


class CompanyLookupView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        query = request.query_params["query"]
        consolidation = request.query_params["consolidation"]

        report = FinancialReport()
        corporate_code = report.get_corporate_code(query)

        if str(corporate_code) == CorporateCodeNotFoundError:
            return Response(data={"message": CorporateCodeNotFoundError}, status=status.HTTP_404_NOT_FOUND)
        financial_statements = report.get_financial_statements(
            corporate_code, consolidation_key)
        financial_reports = report.get_financial_reports(
            financial_statements)

        return Response(data={"reports: ": financial_reports}, status=status.HTTP_200_OK)
