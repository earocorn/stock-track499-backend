from django.db import models
import datetime


class PurchaseOrder(models.Model):
    # ID already auto-populates, dont need to specify
    PO_number = models.IntegerField()
    part_number = models.TextField(default='default value', blank=False, null=False)
    supplier_id = models.IntegerField()
    qty = models.IntegerField()
    due_date = models.DateField()
    created = models.DateField()
    value = models.FloatField() # Stores current active price at time of receipt, * QTY moved
    customer_id =models.TextField(default='default value', blank=False, null=False)
    is_outbound = models.BooleanField()
