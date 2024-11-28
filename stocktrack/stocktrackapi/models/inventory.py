from django.db import models

# List of available parts
class Part(models.Model):
    part_number = models.TextField(default='default value', blank=False, null=False)
    # manufacturer_ID = models.IntegerField()
    supplier_ID = models.IntegerField()
    lead_time = models.IntegerField() # Days from order to delivery?
    inbound_price = models.FloatField()
    outbound_price = models.FloatField()  
    stock_level = models.IntegerField()
    reorder_point = models.IntegerField()  
    # storage_bin = models.TextField(default='default value', blank=False, null=False)   