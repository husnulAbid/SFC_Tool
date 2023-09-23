from rest_framework import serializers

from .models import api_over_time_data


class Totat_Consumption_Over_Time_Serializer(serializers.ModelSerializer):
    class Meta:
        model = api_over_time_data
        fields = ["country", "start_year", "end_year", "beef_consumption", "pig_consumption", "poultry_consumption", "sheep_consumption"]
        