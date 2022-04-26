from django.db import models
from core.models import TimeStampModel

class Payment(TimeStampModel):
    class Status(models.IntegerChoices):
        before_delivery = 1
        on_delivery = 2
        complete_delivery = 3
        cancel_delivery = 4

    status = models.IntegerField(choices=Status.choices, null=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "payments"