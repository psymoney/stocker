from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status


class CompanyLookupView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        corporate_name = request.query_params["corporate_name"]
        consolidation_key = request.query_params["consolidation_key"]
        if consolidation_key == "True":
            consolidation_key = "CFS"
        else:
            consolidation_key = "OFS"

        corporate_code = get_corporate_code(corporate_name)

        financials = CompanyLookupView.get_financials(
            corporate_code, consolidation_key)
        for i in range(1, 100):
            print(financials[i])

        print(
            f"corporate_name = {corporate_name} '\n'consolidation_key = {consolidation_key}")

        def get_corporate_code(name):
            # TODO(SY): uncommnet below codes after implementing get_corporate_code method
            #corpList = request.data()
            # if name in corpList:
            return "00126380"

        return Response(data={"corporate_name": corporate_name, "consolidation_key": consolidation_key}, status=status.HTTP_200_OK)

    def get_financials(corporate_code, consolidation_key):
        URI = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
        API_key = "d3f02b844b4afaa11b10e188bc7a092fc1a63f25"
        business_year = 2019
        report_code = 11011
        encText = "crtfc_key=" + API_key + "&corp_code=" + corporate_code + \
            "&bsns_year=" + str(business_year) + "&reprt_code=" + \
            str(report_code) + "&fs_div=" + consolidation_key
        data_request = URI + encText
        finanacial_data = data_request.data
        return finanacial_data

    def get_financial_reports(financials):
        return "abc"
