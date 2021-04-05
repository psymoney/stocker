from django.db import models


class Corporation(models.Model):
    class Meta:
        db_table = "corporation"

    code = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255, null=False)
    ticker = models.CharField(max_length=255, null=False)
