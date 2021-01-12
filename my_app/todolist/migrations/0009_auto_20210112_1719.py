# Generated by Django 3.1.4 on 2021-01-12 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0008_auto_20210112_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocol_type',
            name='fields',
            field=models.CharField(choices=[('forename', 'First name'), ('surname', 'Second name'), ('yearLevel', 'year level'), ('arrivalDate', 'when joining roll'), ('leavingDate', 'when leaving roll')], default='', max_length=50),
        ),
    ]
