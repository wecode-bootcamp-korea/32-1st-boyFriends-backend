from django.db import models
from core.models import TimeStampModel

class Product(TimeStampModel):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    sale = models.IntegerField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "products"

class Image(TimeStampModel):
    image_urls = models.URLField(max_length=2000)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "images"

class Thumbnail(TimeStampModel):
    image_urls = models.URLField(max_length=2000)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "thumbnails"
    
class Description(TimeStampModel):
    descriptions = models.CharField(max_length=200)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "descriptions"

class Category(TimeStampModel):
    class Main(models.IntegerChoices):
        toy = 1
        apparel = 2
        digital = 3

    class Sub(models.IntegerChoices):
        big_toy = 1
        small_toy = 2
        short_sleeve = 3
        long_sleeve = 4
        phone_case = 5
        small_appliance = 6

    main = models.IntegerField(choices=Main.choices) 
    sub = models.IntegerField(choices=Sub.choices) 

    class Meta:
        db_table = "categories"

class Review(TimeStampModel):
    stars = models.IntegerField()
    comment = models.CharField(max_length=200)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "reviews"

class SizeStock(TimeStampModel):
    class Size(models.IntegerChoices):
        small = 1
        medium = 2
        large = 3

    size = models.IntegerField(choices=Size.choices)
    stock = models.IntegerField()
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "sizes"