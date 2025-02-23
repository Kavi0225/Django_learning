# Generated by Django 5.1.5 on 2025-01-28 11:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_alter_destination_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='desc',
            field=models.TextField(),
        ),
        migrations.CreateModel(
            name='DestinationDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(max_length=100)),
                ('place_description', models.TextField()),
                ('place_image', models.ImageField(upload_to='destination_details/')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='travel.destination')),
            ],
        ),
    ]
