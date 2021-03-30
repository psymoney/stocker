from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import favorite_service as favoriteservice
from ..financials.services import financial_report_service as report_service
from ..financials.services import financial_statement_service as statement_service
from ..rest import auth_header
from ..user.services import token_service as tokenservice

MalformedRequestError = 'malformed request'
EmptyCorporateCodeError = 'empty corporate code'
EmptyCorporateNameError = 'empty corporate name'
EmptyConsolidationError = 'empty consolidation'


class FavoriteView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        token_service = tokenservice.TokenService()
        token = auth_header.get_token(request.headers)

        payload, error_message = token_service.parse_token(token)
        if not payload:
            return Response(data={"message: ": error_message}, status=status.HTTP_403_FORBIDDEN)

        email = payload['email']
        body = request.data

        if 'corporateCode' not in body or 'corporateName' not in body or 'consolidation' not in body:
            return Response(data={"message: ": MalformedRequestError}, status=status.HTTP_400_BAD_REQUEST)

        favorite_service = favoriteservice.FavoriteService()

        duplicate_result = favorite_service.check_duplicate(email, body['corporateName'], body['corporateCode'],
                                                            body['consolidation'])
        if duplicate_result:
            deletion_result = favorite_service.delete_favorite(email, body['corporateName'], body['corporateCode'],
                                                               body['consolidation'])
            if deletion_result:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            creation_result = favorite_service.create_favorite(email, body['corporateName'], body['corporateCode'],
                                                               body['consolidation'])
            if creation_result:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        token_service = tokenservice.TokenService()
        token = auth_header.get_token(request.headers)

        payload, error_message = token_service.parse_token(token)
        if not payload:
            return Response(data={"message: ": error_message}, status=status.HTTP_403_FORBIDDEN)

        email = payload['email']

        favorite_service = favoriteservice.FavoriteService()
        result = favorite_service.get_favorites(email)

        if result is type(str):
            return Response(data={"message: ": result}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={"list: ": result}, status=status.HTTP_200_OK)


class FavoriteReportView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        token_service = tokenservice.TokenService()
        token = auth_header.get_token(request.headers)

        payload, error_message = token_service.parse_token(token)
        if not payload:
            return Response(data={"message: ": error_message}, status=status.HTTP_403_FORBIDDEN)

        query = request.query_params["corporateCode"]
        consolidation = request.query_params["consolidation"]

        if not query or not consolidation:
            return Response(data={"message: malformed request"}, status=status.HTTP_400_BAD_REQUEST)

        financial_report_service = report_service.FinancialReportService()
        financial_statement_service = statement_service.FinancialStatementService()

        financial_statement = financial_statement_service.get_financial_statements(query, consolidation)
        financial_reports = financial_report_service.get_financial_reports(financial_statement)

        return Response(data={'reports: ': financial_reports}, status=status.HTTP_200_OK)
