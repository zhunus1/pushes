# Generated by Django 3.1.2 on 2020-10-22 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(choices=[('CFX', 'Carfax'), ('ADV', 'Adverts'), ('PRK', 'Aparking'), ('GGG', 'Garage')], max_length=3)),
                ('state', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.PositiveIntegerField()),
                ('is_notification', models.BooleanField(default=True)),
                ('data', models.JSONField()),
                ('is_broadcast', models.BooleanField(default=False)),
                ('offset', models.PositiveIntegerField(blank=True, null=True)),
                ('limit', models.PositiveIntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('service', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='notifications.service')),
            ],
        ),
    ]
