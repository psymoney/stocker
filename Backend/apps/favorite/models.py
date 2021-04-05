from django.db import models
from ..user.models import User


class Favorite(models.Model):
    class Meta:
        db_table = 'favorite'

    id = models.AutoField(primary_key=True)
    user_email = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_query_name='User.email'
                                   )
    corporate_name = models.CharField(max_length=255, null=False)
    corporate_code = models.CharField(max_length=255, null=False)
    consolidation = models.CharField(max_length=255, null=False)