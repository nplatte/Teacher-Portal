# Generated by Django 2.2.2 on 2019-07-15 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Class', '0004_auto_20190709_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]