# Generated by Django 4.2.7 on 2023-12-27 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_alter_course_code_alter_course_term_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='year',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='course',
            name='term',
            field=models.CharField(default='', max_length=20),
        ),
    ]
