from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status


class CompView(APIView):
    renderer_classes = [JSONRenderer]
    corporation_name = ""
    consolidation = ""

    def get(self, request):
        //TODO(SY): uncomment below codes after implementing the get function
        # corporation_name
        # corporation_code = get_corporation_code(corporation_name)
        # financials = get_financials(corporation_code, consolidation)
        # print(financials)

        # get_financial_reports(financials)

        return Response(data={"Hello": "world"}, status=status.HTTP_200_OK)

    def post(self, request):
        name = request.query_params["name"]
        cons = request.query_params["cons"]

        set_corpName(name)
        set_fsDiv(cons)
        corporation_code = CompView.get_corporation_code(name)

        financials = CompView.get_financials(
            corporation_code, CompView.consolidation)
        for i in range(1, 100):
            print(financials[i])

        print(
            f"corporation_name = {CompView.corporation_name} '\n'consolidation = {CompView.consolidation}")

        def set_corpName(name):
            CompView.corporation_name = name

        def set_fsDiv(isCons):
            if isCons == "True":
                CompView.consolidation = "CFS"
            else:
                CompView.consolidation = "OFS"

        return Response(data={"corporation_name": CompView.corporation_name, "consolidation": CompView.consolidation}, status=status.HTTP_200_OK)

    def get_financials(corporation_code, consolidation):
        URI = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
        crtfcKey = "d3f02b844b4afaa11b10e188bc7a092fc1a63f25"
        bsnsYear = 2019
        reportCode = 11011
        encText = "crtfc_key=" + crtfcKey + "&corp_code=" + corporation_code + \
            "&bsns_year=" + str(bsnsYear) + "&reprt_code=" + \
            str(reportCode) + "&fs_div=" + consolidation
        finanacial_data = urllib.request.Request(URI + encText)
        return finanacial_data

    def get_corporation_code(name):
        //TODO(SY): uncommnet below codes after implementing get_corporation_code method
        #corpList = request.data()
        # if name in corpList:
        return "00126380"

    def get_financial_reports(financials):
        return "abc"
