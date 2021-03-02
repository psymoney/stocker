from django.db import models

class User(models.User):
    class Meta:
        db_table = "user"

    id = models.IntegerField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
