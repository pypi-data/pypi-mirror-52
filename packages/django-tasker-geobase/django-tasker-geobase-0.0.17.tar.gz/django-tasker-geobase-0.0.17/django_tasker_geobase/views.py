from pprint import pprint

from django.shortcuts import render
from django.test import TestCase
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
