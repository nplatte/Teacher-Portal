# Generated by Django 2.2.2 on 2019-07-15 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Class', '0005_assignment_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]