from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

# TODO(SY): remove index & error view after implementing financials API


class IndexView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        return Response(data={"Hello": "World"}, status=status.HTTP_200_OK)

    def post(self, request):
        body = request.data
        token = request.query_params["token"]
        print(f"Body = {body} token = {token}")

        return Response(data={"post": "poooost"}, status=status.HTTP_200_OK)


class ErrorView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        return Response(data={"Msg": 1234}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
