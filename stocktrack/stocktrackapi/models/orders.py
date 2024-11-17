from django.db import models

class PurchaseOrders(models.Model):
    # ID already auto-populates, dont need to specify
    PO_number = models.IntegerField()
    part_number = models.TextField(default='default value', blank=False, null=False)
    manufacturer_id = models.IntegerField()
    supplier_id = models.IntegerField()
    order_date = models.DateField()
    qty = models.IntegerField()
    due_date = models.DateField()
    received_date = models.DateField()
    value = models.FloatField() # Stores current active price at time of receipt, * QTY moved
    customer_id = models.IntegerField()
    movement_type = models.IntegerField()
