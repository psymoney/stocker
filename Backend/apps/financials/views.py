from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .services import financial_report_service as report_service
from .services import financial_statement_service as statement_service


class CompanyLookupView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        query = request.query_params["query"]
        consolidation = request.query_params["consolidation"]

        financial_report_service = report_service.FinancialReportService()
        financial_statement_service = statement_service.FinancialStatementService()
        corporate_code = financial_report_service.get_corporate_code(query)

        if corporate_code == report_service.CorporateCodeNotFoundError:
            return Response(data={"message": report_service.CorporateCodeNotFoundError}, status=status.HTTP_404_NOT_FOUND)
        financial_statements = financial_statement_service.get_financial_statements(
            corporate_code, consolidation)
        financial_reports = financial_report_service.get_financial_reports(
            financial_statements)

        return Response(data={"reports: ": financial_reports}, status=status.HTTP_200_OK)
