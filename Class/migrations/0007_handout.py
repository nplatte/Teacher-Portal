# Generated by Django 2.2.2 on 2019-07-30 00:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Class', '0006_auto_20190715_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Handout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=25)),
                ('handout', models.FileField(upload_to='')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Class.Course')),
            ],
        ),
    ]