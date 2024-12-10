from django.db import models

# List of available parts
class Part(models.Model):
    part_name = models.TextField(default='Unknown Item', blank=False, null=False)
    part_number = models.IntegerField(unique=True, blank=False, null=False)
    supplier_id = models.IntegerField()
    lead_time = models.IntegerField(default=2) # Days from order to delivery?
    inbound_price = models.FloatField()
    outbound_price = models.FloatField()  
    stock_level = models.IntegerField(default=0)
    reorder_point = models.IntegerField()
    status = models.TextField(default='In Stock', blank=False, null=False)


#     def set_stock_level(self, ):
        