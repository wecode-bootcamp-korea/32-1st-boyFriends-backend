from django.db   import models
from core.models import TimeStampModel

class Cart(TimeStampModel):
    user    = models.ForeignKey("users.User", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    count   = models.IntegerField()

    class Meta:
        db_table = "carts"

class Order(TimeStampModel):
    order_number = models.CharField(max_length=50)
    user         = models.ForeignKey("users.User", on_delete=models.CASCADE)
    order_status = models.ForeignKey("OrderStatus", on_delete=models.CASCADE)

    class Meta:
        db_table = "orders"

class OrderStatus(models.Model):
    status = models.CharField(max_length=20)

    class Meta:
        db_table = "order_statuses"

class OrderItem(TimeStampModel):
    order             = models.ForeignKey("Order", on_delete=models.CASCADE)
    count             = models.IntegerField()
    product           = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    order_item_status = models.ForeignKey("OrderItemStatus", on_delete=models.CASCADE)
    order_shipment    = models.ForeignKey("OrderShipment", on_delete=models.CASCADE)

    class Meta:
        db_table = "order_items"

class OrderItemStatus(models.Model):
    status = models.CharField(max_length=20)

    class Meta:
        db_table = "order_item_statuses"

class OrderShipment(TimeStampModel):
    tracking_number = models.CharField(max_length=50)
    company         = models.CharField(max_length=20)
    
    class Meta:
        db_table = "order_shipments"