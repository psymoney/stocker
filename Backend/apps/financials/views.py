from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .services import financial_report_service as report_service
from .services import financial_statement_service as statement_service
from ..user.services import token_service as tokenservice
from ..user.services import sign_in_service


class CompanyLookupView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        token_service = tokenservice.TokenService()
        header = request.headers

        # TODO(SY): add authorization method
        if 'Authorization' not in header:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if header['Authorization'].split()[0] != 'Bearer':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token = header['Authorization'].split()[1]
        authorization_result = token_service.verify_token(token)

        if authorization_result == sign_in_service.UserNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif authorization_result == tokenservice.InvalidTokenError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif authorization_result == tokenservice.DecodeError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif authorization_result == tokenservice.InvalidSignatureError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif authorization_result:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        query = request.query_params["query"]
        consolidation = request.query_params["consolidation"]

        if not query or not consolidation:
            return Response(data={"message: data not given"}, status=status.HTTP_400_BAD_REQUEST)

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
