from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
import urllib.request
from . import views
from .views import *

# TODO(SY): remove index & error view after implementing financials API


class CompView(APIView):
    renderer_classes = [JSONRenderer]
    corpName = ""
    fsDiv = ""

    def get(self, request):
        # corpName
        # corpCode = get_corpCode(corpName)
        # financials = get_financials(corpCode, fsDiv)
        # print(financials)

        # get_financial_reports(financials)

        return Response(data={"Hello": "world"}, status=status.HTTP_200_OK)

    def post(self, request):
        name = request.query_params["name"]
        cons = request.query_params["cons"]

        CompView.set_corpName(name)
        CompView.set_fsDiv(cons)
        corpCode = CompView.get_corpCode(name)

        financials = CompView.get_financials(corpCode, CompView.fsDiv)
        for i in range(1, 100):
            print(financials[i])

        print(f"corpName = {CompView.corpName} '\n'fsDiv = {CompView.fsDiv}")
        return Response(data={"corpName": CompView.corpName, "fsDiv": CompView.fsDiv}, status=status.HTTP_200_OK)

    def get_financials(corpCode, fsDiv):
        URI = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
        crtfcKey = "d3f02b844b4afaa11b10e188bc7a092fc1a63f25"
        bsnsYear = 2019
        reportCode = 11011
        encText = "crtfc_key=" + crtfcKey + "&corp_code=" + corpCode + \
            "&bsns_year=" + str(bsnsYear) + "&reprt_code=" + \
            str(reportCode) + "&fs_div=" + fsDiv
        fData = urllib.request.Request(URI + encText)
        return fData

    def set_corpName(name):
        CompView.corpName = name

    def set_fsDiv(isCons):
        if isCons == "True":
            CompView.fsDiv = "CFS"
        else:
            CompView.fsDiv = "OFS"

    def get_corpCode(name):
        #corpList = request.data()
        # if name in corpList:
        return "00126380"

    def get_financial_reports(financials):
        return "abc"
