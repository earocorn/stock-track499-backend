# Generated by Django 5.1.4 on 2024-12-06 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocktrackapi', '0002_part_purchaseorder_suppliers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseorder',
            old_name='PO_number',
            new_name='po_number',
        ),
    ]
