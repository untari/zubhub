# Generated by Django 2.2.7 on 2021-04-14 05:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0004_auto_20210413_2355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='published',
        ),
        migrations.CreateModel(
            name='TreeComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('text', models.CharField(max_length=10000)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tree_comments', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tree_comments', to='projects.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]