from django.db import models
from enum import Enum

ROLE_CONSTRAINTS = (
    ('admin', 'Admin'),
    ('employee', 'Employee'),
    ('manager', 'Manager'),
    ('customer', 'Customer'),
)

class Role(Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    EMPLOYEE = 'employee'
    CUSTOMER = 'customer'

    def get_all_roles():
        return {role.value for role in Role}

    def is_valid(role):
        all_roles = Role.get_all_roles()
        if role is None:
            return False
        if isinstance(role, str):
            return role in all_roles
        return role.value in all_roles
    
    def is_admin_or_manager(role):
        if role is None:
            return False
        if isinstance(role, str):
            return role == Role.ADMIN.value or role == Role.MANAGER.value
        return role == Role.ADMIN or role == Role.MANAGER
    
    def is_employee(role):
        if role is None:
            return False
        if isinstance(role, str):
            return role == Role.EMPLOYEE.value
        return role == Role.EMPLOYEE
    
    def is_customer(role):
        if role is None:
            return False
        if isinstance(role, str):
            return role == Role.CUSTOMER.value
        return role == Role.CUSTOMER


class StockTrackUser(models.Model):
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    uid = models.CharField(max_length=50, unique=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    profile_img = models.URLField(default='', blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CONSTRAINTS, blank=False, null=False, default='customer')

    class Meta:
        # Always order users based on 'created' field
        ordering = ['created']