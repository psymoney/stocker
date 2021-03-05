from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .services import sign_up_service
from .services import sign_in_service


class SignupView(APIView):
    renderer_class = [JSONRenderer]

    def post(self, request):
        email = request.data["email"]
        user_name = request.data["userName"]
        password = request.data["password"]
        signup = sign_up_service.SignUpService()
        result = signup.create_user_account(email, user_name, password)

        if result == sign_up_service.DuplicateEmailExistError:
            return Response(data={"message: ": result}, status=status.HTTP_409_CONFLICT)
        elif result == sign_up_service.InvalidEmailError:
            return Response(data={"message: ": result}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif result == sign_up_service.InvalidUserNameError:
            return Response(data={"message: ": result}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif result == sign_up_service.InvalidPasswordError:
            return Response(data={"message: ": result}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif result:
            return Response(data={"message: ": result}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


# TODO(SY): Add token service
class SigninView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        login = sign_in_service.SignInService()
        result = login.sign_in(email, password)
        if result == sign_in_service.UserNotFoundError:
            return Response(data={"Message: ": result}, status=status.HTTP_404_NOT_FOUND)
        elif result == sign_in_service.WrongPasswordError:
            return Response(data={"Message: ": result}, status=status.HTTP_403_FORBIDDEN)

        return Response(data={"Success"}, status=status.HTTP_200_OK)

