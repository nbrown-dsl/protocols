# Generated by Django 3.1.4 on 2021-01-27 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0005_auto_20210127_1159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listfields',
            old_name='firstname',
            new_name='field',
        ),
        migrations.RemoveField(
            model_name='listfields',
            name='surname',
        ),
    ]