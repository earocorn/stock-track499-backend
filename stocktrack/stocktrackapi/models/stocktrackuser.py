from django.db import models

ROLES = (
    ('admin', 'Admin'),
    ('employee', 'Employee'),
    ('manager', 'Manager'),
    ('customer', 'Customer'),
)

class StockTrackUser(models.Model):
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    uid = models.CharField(max_length=50, unique=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    profile_img = models.URLField(default='')
    role = models.CharField(max_length=20, choices=ROLES, blank=False, null=False, default='customer')

    class Meta:
        # Always order users based on 'created' field
        ordering = ['created']