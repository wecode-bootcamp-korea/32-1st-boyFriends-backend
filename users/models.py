from django.db   import models
from core.models import TimeStampModel

class User(TimeStampModel):
    name         = models.CharField(max_length=10)
    email        = models.CharField(max_length=50, unique=True)
    password     = models.CharField(max_length=200)
    address      = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    gender       = models.CharField(max_length=2)
    age          = models.IntegerField()

    class Meta:
        db_table = "users"