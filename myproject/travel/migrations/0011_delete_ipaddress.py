# Generated by Django 5.1.5 on 2025-02-03 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0010_ipaddress_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IPAddress',
        ),
    ]
