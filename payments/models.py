from django.db import models
from core.models import TimeStampModel

# Create your models here.

# manytomany
class Payment(TimeStampModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "payments"