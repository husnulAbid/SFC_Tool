from django.db import models


class Sfc_tool_User(models.Model):
    name = models.CharField(max_length = 200)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
