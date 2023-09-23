from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, serializers

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

from .serializers import Totat_Consumption_Over_Time_Serializer


##### Need to implement more error handling, saving to db

class TotatConsumptionOverTime(APIView):
    
    ###

    # Sample Get Request:
    # {base_url}/data_analysis/meat_consumption/api_1/all_type_countrywise/?country=NZL&start_year=1994&end_year=2020

    ###
    
    def get(self, request):
        country = request.GET.get('country')
        start_year = int(request.GET.get('start_year'))
        end_year = int(request.GET.get('end_year'))

        if not country:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not start_year:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not end_year:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        beef_consumption, pig_consumption, poultry_consumption, sheep_consumption =  self.calculate_total_consumption(country, start_year, end_year)

        result_ = {
            "country": f"{country}",
            "start_year": f"{start_year}",
            "end_year": f"{end_year}",
            "beef_consumption": f"{beef_consumption}",
            "pig_consumption": f"{pig_consumption}",
            "poultry_consumption": f"{poultry_consumption}",
            "sheep_consumption": f"{sheep_consumption}",
        }

        serializer = Totat_Consumption_Over_Time_Serializer(data=result_)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    

    ##### Need to improve this part

    def calculate_total_consumption(self, country, start_year, end_year):
        api_endpoint = f'{os.environ.get("FLASK_APP_ENDPOINT")}/analysis/meat_consumption_time?country={country}&start={start_year}&end={end_year}'
        headers = {}

        try:
            response = requests.get(url=api_endpoint, headers=headers)

            beef_consumption = response.json()['beef']
            pig_consumption = response.json()['pig']
            poultry_consumption = response.json()['poultry']
            sheep_consumption = response.json()['sheep']
        except:
            beef_consumption = 'API Error'
            pig_consumption = 'API Error'
            poultry_consumption = 'API Error' 
            sheep_consumption = 'API Error'

        return beef_consumption, pig_consumption, poultry_consumption, sheep_consumption
    


class AvailableCountries(APIView):
    
    ###

    # Sample Get Request:
    # {base_url}/data_analysis/meat_consumption/api_1/available_countries/

    ###
    
    def get(self, request):
        api_endpoint = f'{os.environ.get("FLASK_APP_ENDPOINT")}/analysis/meat_consumption_time/countries'
        headers = {}

        try:
            response = requests.get(url=api_endpoint, headers=headers)
            countries = response.json()['countries']
        except:
            countries = 'API Error'
        
        result_ = {
            "countries": f"{countries}",
        }

        return Response(result_, status=status.HTTP_200_OK)


class StartAndEndYear(APIView):
    
    ###

    # Sample Get Request:
    # {base_url}/data_analysis/meat_consumption/api_1/start_and_end_year/

    ###
    
    def get(self, request):
        api_endpoint = f'{os.environ.get("FLASK_APP_ENDPOINT")}/analysis/meat_consumption_time/start_and_end_year'
        headers = {}

        try:
            response = requests.get(url=api_endpoint, headers=headers)
            end_year = response.json()['end_year']
            start_year = response.json()['start_year']
        except:
            end_year = 'API Error'
            start_year = 'API Error'
        
        result_ = {
            "end_year": f"{end_year}",
            "start_year": f"{start_year}",
        }

        return Response(result_, status=status.HTTP_200_OK)
