import uuid

from django.db   import models
from core.models import TimeStampModel

class Cart(TimeStampModel):
    user      = models.ForeignKey("users.User", on_delete=models.CASCADE)
    product   = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    count     = models.PositiveIntegerField()
    check_box = models.BooleanField(default=True)
    option    = models.ForeignKey("products.Size", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "carts"

class Order(TimeStampModel):
    order_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user         = models.ForeignKey("users.User", on_delete=models.CASCADE)
    order_status = models.ForeignKey("OrderStatus", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "orders"

class OrderStatus(models.Model):
    status = models.CharField(max_length=20)

    class Meta:
        db_table = "order_statuses"

class OrderItem(TimeStampModel):
    count             = models.PositiveIntegerField()
    order             = models.ForeignKey("Order", on_delete=models.CASCADE)
    product           = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    order_item_status = models.ForeignKey("OrderItemStatus", on_delete=models.SET_NULL, null=True)
    order_shipment    = models.ForeignKey("OrderShipment", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "order_items"

class OrderItemStatus(models.Model):
    status = models.CharField(max_length=20)

    class Meta:
        db_table = "order_item_statuses"

class OrderShipment(TimeStampModel):
    tracking_number  = models.CharField(max_length=50, unique=True)
    carrier          = models.ForeignKey("Carrier", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "order_shipments"

class Carrier(TimeStampModel):
    carriers = models.CharField(max_length=20)

    class Meta:
        db_table = "carriers"