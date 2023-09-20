from rest_framework import serializers

from .models import Sfc_tool_User


class Sfc_tool_User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sfc_tool_User
        fields = ["name", "email", "password"]