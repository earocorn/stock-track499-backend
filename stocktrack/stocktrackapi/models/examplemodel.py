from django.db import models

ROLES = (
    ('admin', 'Admin'),
    ('employee', 'Employee'),
    ('manager', 'Manager'),
    ('customer', 'Customer'),
)

class ExampleModel(models.Model):
    # ID already auto-populates, dont need to specify
    boolean_field = models.BooleanField()
    date_field = models.DateField()
    datetime_field = models.DateTimeField()
    integer_field = models.IntegerField()
    float_field = models.FloatField()
    example_constraints = models.TextField(default='default value',
                                           blank=False,
                                           null=False)

# Used to track type of transaction and control action against DB
class MovementTypes(models.Model):
    # ID already auto-populates, dont need to specify
    movement_type = models.IntegerField()
    description = models.TextField(default='default value', blank=False, null=False)

# Used to assign a unique ID to a customer
class Customers(models.Model):
    # ID already auto-populates, dont need to specify
    customer_ID = models.IntegerField()
    customer_name = models.TextField(default='default value', blank=False, null=False)

# Used to assign a unique ID to a manufacturer
class Manufacturers(models.Model):
    # ID already auto-populates, dont need to specify
    manufacturer_ID = models.IntegerField()
    manufacturer_name = models.TextField(default='default value', blank=False, null=False)

    # Used to assign a unique ID to a supplier
class Suppliers(models.Model):
    # ID already auto-populates, dont need to specify
    supplier_ID = models.IntegerField()
    supplier_name = models.TextField(default='default value', blank=False, null=False)

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

class PartsList(models.Model):
    # ID already auto-populates, dont need to specify
    part_number = models.TextField(default='default value', blank=False, null=False)
    manufacturer = models.IntegerField()
    supplier = models.IntegerField()
    lead_time = models.IntegerField()
    price = models.FloatField()  

class Stock(models.Model):
    # ID already auto-populates, dont need to specify
    part_number = models.TextField(default='default value', blank=False, null=False)
    stock_level = models.IntegerField()
    reorder_point = models.IntegerField()  

class WarehouseTasks(models.Model):
    # ID already auto-populates, dont need to specify
    warehouse_task = models.IntegerField()
    movement_type = models.IntegerField()
    part_number = models.TextField(default='default value', blank=False, null=False)
    qty = models.IntegerField()
    value = models.FloatField() # Stores current active price at time of movement, * QTY moved
