# Generated by Django 5.1.3 on 2024-11-27 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExampleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boolean_field', models.BooleanField()),
                ('date_field', models.DateField()),
                ('datetime_field', models.DateTimeField()),
                ('integer_field', models.IntegerField()),
                ('float_field', models.FloatField()),
                ('example_constraints', models.TextField(default='default value')),
            ],
        ),
        migrations.CreateModel(
            name='StockTrackUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('uid', models.CharField(max_length=50, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('profile_img', models.URLField(default='')),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('employee', 'Employee'), ('manager', 'Manager'), ('customer', 'Customer')], default='customer', max_length=20)),
            ],
            options={
                'ordering': ['created'],
            },
        ),

    ]
