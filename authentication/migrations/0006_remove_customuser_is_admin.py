# Generated by Django 3.1.4 on 2021-01-15 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_customuser_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_admin',
        ),
    ]
