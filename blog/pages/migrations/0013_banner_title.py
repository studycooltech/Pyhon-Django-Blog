# Generated by Django 3.2 on 2021-04-22 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_auto_20210421_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='title',
            field=models.CharField(default='t', max_length=120),
        ),
    ]
