# Generated by Django 3.0.5 on 2020-12-04 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0003_list_priority'),
    ]

    operations = [
        migrations.CreateModel(
            name='persons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(default='', max_length=400)),
            ],
        ),
        migrations.AddField(
            model_name='list',
            name='dueDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='list',
            name='people',
            field=models.ManyToManyField(to='todo_list.persons'),
        ),
    ]
