# Generated by Django 3.1.2 on 2020-10-26 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_auto_20201023_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_notification',
        ),
        migrations.RemoveField(
            model_name='event',
            name='limit',
        ),
        migrations.RemoveField(
            model_name='event',
            name='offset',
        ),
        migrations.AlterField(
            model_name='service',
            name='url',
            field=models.URLField(),
        ),
    ]
