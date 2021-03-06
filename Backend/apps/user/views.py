from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .services import sign_up_service as signup_service
from .services import sign_in_service as signin_service
from .services.token_service import TokenService


class SignupView(APIView):
    renderer_class = [JSONRenderer]

    def post(self, request):
        email = request.data["email"]
        user_name = request.data["userName"]
        password = request.data["password"]
        sign_up_service = signup_service.SignUpService()
        result = sign_up_service.create_user_account(email, user_name, password)

        if result == signup_service.DuplicateEmailExistError:
            return Response(data={"message: ": result}, status=status.HTTP_409_CONFLICT)
        elif result == signup_service.InvalidEmailError:
            return Response(data={"message: ": result}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif result == signup_service.InvalidUserNameError:
            return Response(data={"message: ": result}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif result == signup_service.InvalidPasswordError:
            return Response(data={"message: ": result}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif result:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)


class SigninView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        sign_in_service = signin_service.SignInService()
        result = sign_in_service.sign_in(email, password)
        if result == signin_service.UserNotFoundError:
            return Response(data={"message: ": result}, status=status.HTTP_404_NOT_FOUND)
        elif result == signin_service.WrongPasswordError:
            return Response(data={"message: ": result}, status=status.HTTP_403_FORBIDDEN)
        token_service = TokenService()
        access_token = token_service.create_token(request.data["email"])
        return Response(data={"accessToken": access_token}, status=status.HTTP_200_OK)

