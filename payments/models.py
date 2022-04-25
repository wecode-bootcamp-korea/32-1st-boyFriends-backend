from tkinter import CASCADE
from django.db import models
from core.models import TimeStampModel

# Create your models here.

# manytomany
class Payment(TimeStampModel):
    user = models.ForeignKey("User", on_delete=CASCADE)
    product = models.ForeignKey("Product", on_delete=CASCADE)

    class Meta:
        db_table = "payments"