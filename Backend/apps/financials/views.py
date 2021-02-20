from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status


class CompanyLookupView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        corporateName = request.query_params["corporateName"]
        consolidationKey = request.query_params["consolidationKey"]
        if consolidationKey == "True":
            consolidationKey = "CFS"
        else:
            consolidationKey = "OFS"

        corporate_code = get_corporate_code(corporateName)

        financials = get_financials()
        for i in range(1, 100):
            print(financials[i])

        print(
            f"corporateName = {corporateName} '\n'consolidationKey = {consolidationKey}")

        def get_corporate_code(name):
            # TODO(SY): uncommnet below codes after implementing get_corporate_code method
            #corpList = request.data()
            # if name in corpList:
            return "00126380"

        return Response(data={"corporateName": corporateName, "consolidationKey": consolidationKey}, status=status.HTTP_200_OK)

        def get_financials():
            URI = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
            API_key = "d3f02b844b4afaa11b10e188bc7a092fc1a63f25"
            business_year = 2019
            report_code = 11011
            parameter_text = "crtfc_key=" + API_key + "&corp_code=" + corporate_code + \
                "&bsns_year=" + str(business_year) + "&reprt_code=" + \
                str(report_code) + "&fs_div=" + consolidationKey

            # TODO(SY): request financial data to opendart API
            data_request = URI + parameter_text
            financial_data = data_request.data
            return financial_data

        def get_financial_reports(financials):
            return "abc"
