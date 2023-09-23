from django.db import models


class api_over_time_data(models.Model):
    
    id = models.CharField(max_length = 180, primary_key=True)
    country = models.TextField(max_length = 100)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    beef_consumption = models.TextField(max_length = 100)
    pig_consumption = models.TextField(max_length = 100)
    poultry_consumption = models.TextField(max_length = 100)
    sheep_consumption = models.TextField(max_length = 100)

    
    def __str__(self):
        return self.task