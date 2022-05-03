from django.db   import models
from core.models import TimeStampModel

class Product(TimeStampModel):
    name           = models.CharField(max_length=50)
    price          = models.PositiveIntegerField()
    discount       = models.PositiveIntegerField(null=True)
    category       = models.ForeignKey("Category", on_delete=models.CASCADE)
    caution        = models.ForeignKey("Caution", on_delete=models.SET_NULL, null=True)
    product_status = models.ForeignKey("ProductStatus", on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = "products"

class ProductStatus(models.Model):
    status = models.CharField(max_length=10)

    class Meta:
        db_table = "product_statuses"

class Caution(models.Model):
    description = models.CharField(max_length=500)

    class Meta:
        db_table = "cautions"

class Image(models.Model):
    image_urls = models.URLField(max_length=2000)
    product    = models.ForeignKey("Product", on_delete=models.CASCADE, null=True)
    image_type = models.ForeignKey("ImageType", on_delete=models.CASCADE)
    review     = models.ForeignKey("Review", on_delete=models.CASCADE ,null=True)
    category   = models.ForeignKey("Category", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "images"

class ImageType(models.Model):
    type = models.CharField(max_length=10)

    class Meta:
        db_table = "image_types"
    
class MainCategory(models.Model):
    main = models.CharField(max_length=10)

    class Meta:
        db_table = "main_categories"

class Category(models.Model):
    sub           = models.CharField(max_length=10)
    main_category = models.ForeignKey("MainCategory", on_delete=models.CASCADE)

    class Meta:
        db_table = "categories"

class Review(TimeStampModel):
    rating   = models.PositiveIntegerField()
    comment = models.CharField(max_length=200)
    user    = models.ForeignKey("users.User", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "reviews"

class Size(models.Model):
    size    = models.CharField(max_length=10)
    product = models.ManyToManyField("Stock", through="SizeStock")

    class Meta:
        db_table = "sizes"

class Stock(models.Model):
    stock = models.PositiveIntegerField()

    class Meta:
        db_table = "stocks"        

class SizeStock(TimeStampModel):
    size    = models.ForeignKey("Size", on_delete=models.PROTECT, null=True)
    stock   = models.ForeignKey("Stock", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "size_stock"