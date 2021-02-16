# Generated by Django 3.1.4 on 2021-02-16 13:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0002_auto_20210216_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='list',
            name='people',
        ),
        migrations.AlterField(
            model_name='list',
            name='arrivalDate',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='list',
            name='leavingDate',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]