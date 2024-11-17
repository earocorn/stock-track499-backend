from django.db import models

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