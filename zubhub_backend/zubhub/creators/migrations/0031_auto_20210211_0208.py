# Generated by Django 2.2.7 on 2021-02-11 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('creators', '0030_phonenumber_setting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setting',
            name='creator',
        ),
        migrations.DeleteModel(
            name='PhoneNumber',
        ),
        migrations.DeleteModel(
            name='Setting',
        ),
    ]
