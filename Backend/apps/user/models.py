from django.db import models

class User(models.User):
    class Meta:
        db_table = "user"

    id = models.AutoField()
    name = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
