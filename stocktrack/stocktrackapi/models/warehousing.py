from django.db import models

# Used to track type of transaction and control action against DB
class MovementTypes(models.Model):
    # ID already auto-populates, dont need to specify
    movement_type = models.IntegerField()
    description = models.TextField(default='default value', blank=False, null=False)

class WarehouseTasks(models.Model):
    # ID already auto-populates, dont need to specify
    warehouse_task = models.IntegerField()
    movement_type = models.IntegerField()
    part_number = models.TextField(default='default value', blank=False, null=False)
    qty = models.IntegerField()
    value = models.FloatField() # Stores current active price at time of movement, * QTY moved
