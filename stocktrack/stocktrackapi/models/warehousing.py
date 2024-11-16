from django.db import models

ROLES = (
    ('admin', 'Admin'),
    ('employee', 'Employee'),
    ('manager', 'Manager'),
    ('customer', 'Customer'),
)

class PurchaseOrders(models.Model):
    # ID already auto-populates, dont need to specify
    PO_number = models.IntegerField()
    part_number = models.TextField(default='default value', blank=False, null=False)
    manufacturer = models.IntegerField()
    supplier = models.IntegerField()
    order_date = models.DateField()
    qty = models.IntegerField()
    due_date = models.DateField()
    received_date = models.DateField()
    value = models.FloatField() # Stores current active price at time of receipt, * QTY moved

class WarehouseTasks(models.Model):
    # ID already auto-populates, dont need to specify
    warehouse_task = models.IntegerField()
    movement_type = models.IntegerField()
    part_number = models.TextField(default='default value', blank=False, null=False)
    qty = models.IntegerField()
    value = models.FloatField() # Stores current active price at time of movement, * QTY moved

# Used to track type of transaction and control action against DB
class MovementTypes(models.Model):
    # ID already auto-populates, dont need to specify
    movement_type = models.IntegerField()
    description = models.TextField(default='default value', blank=False, null=False)