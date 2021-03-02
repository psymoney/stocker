from django.db import models


class User(models.Model):
    class Meta:
        db_table = "user"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
