import json
import os

import requests
from django.conf import settings

from rest_framework.views import APIView
from rest_framework import response, request, status
from . import serializer, models, geocoder


class GeoObject(APIView):
    serializer_class = serializer.GeoBase

    def get(self, request: request.Request, geobase: models.Geobase):
        serializer_obj = self.serializer_class(data=geobase.dict())
        if not serializer_obj.is_valid():
            return response.Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)

        return response.Response(serializer_obj.validated_data)


class Search(APIView):
    serializer_class = serializer.Search

    def get(self, request: request.Request):
        serializer_obj = self.serializer_class(data=request.GET)
        if not serializer_obj.is_valid():
            return response.Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)

        result = geocoder.geo(query=serializer_obj.validated_data.get('query'))
        if result:
            return response.Response(result.dict())
        else:
            return response.Response({}, status=status.HTTP_404_NOT_FOUND)


class Suggestion(APIView):
    serializer_class = serializer.Search

    def get(self, request: request.Request):
        serializer_obj = self.serializer_class(data=request.GET)
        if not serializer_obj.is_valid():
            return response.Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)

        data_key = getattr(settings, 'GEOBASE_DADATA', os.environ.get('GEOBASE_DADATA'))
        if not data_key:
            raise Exception("not found key GEOBASE_DADATA")

        res = requests.post(
            url="https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address",
            data=json.dumps({"query": serializer_obj.validated_data.get('query'), "count": 10}),
            headers={
                'Authorization': "Token {token}".format(token=settings.GEOBASE_DADATA),
                'Content-Type': "application/json",
                'Accept': "application/json",
            }
        )

        dadata = []
        if 'suggestions' in res.json():
            for item in res.json().get('suggestions'):
                dadata.append({'value': item.get('value')})

        return response.Response({'result': dadata})
