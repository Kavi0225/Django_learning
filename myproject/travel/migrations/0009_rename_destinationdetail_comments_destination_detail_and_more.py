# Generated by Django 5.1.5 on 2025-02-03 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0008_comments_user_agent_comments_user_ip_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='DestinationDetail',
            new_name='destination_detail',
        ),
        migrations.RenameField(
            model_name='destinationdetail',
            old_name='user_ip',
            new_name='ip_address',
        ),
    ]
