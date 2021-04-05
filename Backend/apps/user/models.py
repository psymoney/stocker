from django.db import models


class User(models.Model):
    class Meta:
        db_table = "user"

    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, null=False)
    user_name = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
