# Generated by Django 2.2.7 on 2021-03-25 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('creators', '0046_auto_20210324_2114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creator',
            name='role',
        ),
    ]