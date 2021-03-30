from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import financial_report_service as report_service
from .services import financial_statement_service as statement_service
from ..rest import auth_header
from ..user.services import token_service as tokenservice

MalformedRequestError = 'malformed request'


class CompanyLookupView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        token_service = tokenservice.TokenService()
        token = auth_header.get_authorization_header(request.headers)

        payload, error_message = token_service.parse_token(token)
        if not payload:
            return Response(data={"message: ": error_message}, status=status.HTTP_403_FORBIDDEN)
        query = request.query_params["query"]
        consolidation = request.query_params["consolidation"]

        if not query or not consolidation:
            return Response(data={"message: ": MalformedRequestError}, status=status.HTTP_400_BAD_REQUEST)

        print(query)
        financial_report_service = report_service.FinancialReportService()
        financial_statement_service = statement_service.FinancialStatementService()
        corporate_code = financial_report_service.get_corporate_code(query)

        if corporate_code == report_service.CorporateCodeNotFoundError:
            return Response(data={"message": report_service.CorporateCodeNotFoundError},
                            status=status.HTTP_404_NOT_FOUND)
        financial_statements = financial_statement_service.get_financial_statements(
            corporate_code, consolidation)
        financial_reports = financial_report_service.get_financial_reports(
            financial_statements)

        return Response(data={"reports: ": financial_reports}, status=status.HTTP_200_OK)
