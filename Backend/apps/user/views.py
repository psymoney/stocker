from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .services.sign_up_service import SignUpService
from .services.sign_in_service import SignInService


class SignupView(APIView):
    renderer_class = [JSONRenderer]

    def post(self, request):
        user_information = request.data
        email = user_information["email"]
        user_name = user_information["userName"]
        password = user_information["password"]
        result = SignUpService.sign_up(self, email, user_name, password)
        if result == True:
            return Response(status=status.HTTP_200_OK)
        return Response(data={"message: ": result}, status=status.HTTP_409_CONFLICT)

class SigninView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        login_information = request.data
        email = login_information["email"]
        password = login_information["password"]
        result = SignInService.sign_in(self, email, password)
        if result == True:
            return Response(data={"Success"}, status=status.HTTP_200_OK)
        return Response(data={"Message: ": result}, status=status.HTTP_409_CONFLICT)

