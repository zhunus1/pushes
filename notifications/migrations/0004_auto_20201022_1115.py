# Generated by Django 3.1.2 on 2020-10-22 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20201022_1113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('created',)},
        ),
    ]