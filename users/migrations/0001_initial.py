# Generated by Django 3.1.2 on 2020-10-22 03:33

from django.db import migrations, models
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DuplicateUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caps_token', models.CharField(blank=True, max_length=70)),
                ('caps_id', models.IntegerField(unique=True, verbose_name='CAPS ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone number')),
                ('email', models.CharField(blank=True, max_length=63, null=True, verbose_name='Email')),
                ('first_name', models.CharField(blank=True, max_length=63, null=True, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=63, null=True, verbose_name='Last name')),
                ('avatar', models.URLField(blank=True, null=True, verbose_name='Avatar')),
                ('thumbnail', models.URLField(blank=True, null=True, verbose_name='Thumbnail')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Birthday')),
                ('last_seen', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last seen')),
                ('gender', models.IntegerField(default=0, verbose_name='Gender')),
                ('is_manager', models.BooleanField(default=False, verbose_name='Is manager')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ('-created',),
            },
        ),
    ]
