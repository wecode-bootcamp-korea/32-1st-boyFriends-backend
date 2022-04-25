from tkinter import CASCADE
from django.db import models
from core.models import TimeStampModel

# Create your models here.
class Product(TimeStampModel):
    name = models.CharField(max_length=50)
    price = models.IntegerField(max_length=10)
    sale = models.IntegerField(max_length=3)
    review = models.ManyToManyField("users.User", through='Review', related_name='product_review')
    payment = models.ManyToManyField("users.User", through='Payment', related_name='product_payment')

    class Meta:
        db_table = "products"

class Image(TimeStampModel):
    image_urls = models.URLField(max_length=2000)
    product = models.ForeignKey("Product", on_delete=CASCADE)

    class Meta:
        db_table = "images"

class Thumbnail(TimeStampModel):
    image_urls = models.URLField(max_length=2000)
    product = models.ForeignKey("Product", on_delete=CASCADE)

    class Meta:
        db_table = "thumbnails"
    
class Description(TimeStampModel):
    descriptions = models.CharField(max_length=200)
    product = models.ForeignKey("Product", on_delete=CASCADE)

    class Meta:
        db_table = "descriptions"

class Category(TimeStampModel):
    class Index(models.IntegerChoices):
        toy = 1
        apparel = 2
        digital = 3

    class SubIndex(models.IntegerChoices):
        big_toy = 1
        small_toy = 2
        short_sleeve = 3
        long_sleeve = 4
        phone_case = 5
        small_appliance = 6

    index = models.IntegerField(db_index=True, choices=Index.choices) 
    sub_index = models.IntegerField(choices=SubIndex.choices) 
    product = models.ForeignKey("Product", on_delete=CASCADE)

    class Meta:
        db_table = "categories"

# manytomany
class Review(TimeStampModel):
    stars = models.IntegerField(max_length=1)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey("User", on_delete=CASCADE)
    product = models.ForeignKey("Product", on_delete=CASCADE)

    class Meta:
        db_table = "reviews"

class SizeStock(TimeStampModel):
    class Size(models.IntegerChoices):
        small = 1
        medium = 2
        large = 3

    size = models.IntegerField(choices=Size.choices)
    stock = models.IntegerField(max_length=1000)
    product = models.ForeignKey("Product", on_delete=CASCADE)

    class Meta:
        db_table = "sizes"