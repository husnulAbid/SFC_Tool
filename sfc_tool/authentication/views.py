from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Sfc_tool_User
from .serializers import Sfc_tool_User_Serializer


class Sfc_tool_User_ApiView(APIView):

    def get(self, request, *args, **kwargs):

        sfc_tool_users = Sfc_tool_User.objects
        serializer = Sfc_tool_User_Serializer(sfc_tool_users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):

        data = {
            'name': request.data.get('name'), 
            'email': request.data.get('email'),
            'password': request.data.get('password')
        }

        serializer = Sfc_tool_User_Serializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)