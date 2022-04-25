from django.db   import models
from core.models import TimeStampModel
# Create your models here.                                                       

class User(TimeStampModel):
    class Gender(models.IntegerChoices):
        male = 1
        female = 2
    
    class Age(models.IntegerChoices):
        teenage = 10
        twenties = 20
        thirties = 30
        forties = 40

    name = models.CharField(max_length=10)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    gender = models.IntegerField(choices=Gender.choices)
    age = models.IntegerField(choices=Age.choices, null=True)

    class Meta:
        db_table = "users"