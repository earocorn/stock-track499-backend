# Generated by Django 5.1.4 on 2024-12-09 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocktrackapi', '0003_remove_purchaseorder_po_number_part_lead_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='status',
            field=models.TextField(default='In Stock'),
        ),
    ]
