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