from django.db import models

ROLES = (
    ('admin', 'Admin'),
    ('employee', 'Employee'),
    ('manager', 'Manager'),
    ('customer', 'Customer'),
)

class PartsList(models.Model):
    # ID already auto-populates, dont need to specify
    part_number = models.TextField(default='default value', blank=False, null=False)
    manufacturer_ID = models.IntegerField()
    supplier_ID = models.IntegerField()
    lead_time = models.IntegerField()
    price = models.FloatField()  

class Stock(models.Model):
    # ID already auto-populates, dont need to specify
    part_number = models.TextField(default='default value', blank=False, null=False)
    stock_level = models.IntegerField()
    reorder_point = models.IntegerField()  