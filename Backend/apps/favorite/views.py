from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from ..user.services import token_service as tokenservice
from ..user.services import sign_in_service
from .services import favorite_service as favoriteservice
from ..financials.services import financial_report_service as report_service
from ..financials.services import financial_statement_service as statement_service


class FavoriteView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
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

        email = token_service.return_email(token)
        body = request.data

        if 'corporateCode' not in body:
            return Response(data={"message: corporateCode not provided"}, status=status.HTTP_400_BAD_REQUEST)
        if 'corporateName' not in body:
            return Response(data={"message: corporateName not provided"}, status=status.HTTP_400_BAD_REQUEST)
        if 'consolidation' not in body:
            return Response(data={"message: consolidation not provided"}, status=status.HTTP_400_BAD_REQUEST)

        favorite_service = favoriteservice.FavoriteService()

        is_duplicate = favorite_service.check_duplicate(email, body['corporateName'], body['corporateCode'], body['consolidation'])
        if is_duplicate:
            deletion_result = favorite_service.delete_favorite(email, body['corporateName'], body['corporateCode'], body['consolidation'])
            if deletion_result:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            creation_result = favorite_service.create_favorite(email, body['corporateName'], body['corporateCode'], body['consolidation'])
            if creation_result:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)

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

        email = token_service.return_email(token)

        favorite_service = favoriteservice.FavoriteService()
        favorites = favorite_service.get_favorites(email)

        if favorites == favoriteservice.DoesNotExistError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif favorites is type(str):
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={"list: ": favorites}, status=status.HTTP_200_OK)

class FavoriteReportView(APIView):
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

        query = request.query_params("corporateCode")
        consolidation = request.query_params("consolidation")

        if not query or not consolidation:
            return Response(data={"message:  data not given"}, status=status.HTTP_400_BAD_REQUEST)

        financial_report_service = report_service.FinancialReportService()
        financial_statement_service = statement_service.FinancialStatementService()

        financial_statement = financial_statement_service.get_financial_statements(query, consolidation)
        financial_reports = financial_report_service.get_financial_reports(financial_statement)

        return Response(data={'reports: ': financial_reports}, status=status.HTTP_200_OK)