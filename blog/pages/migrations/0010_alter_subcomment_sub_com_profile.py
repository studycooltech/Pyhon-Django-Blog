# Generated by Django 3.2 on 2021-04-21 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_subcomment_sub_com_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcomment',
            name='sub_com_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.profile'),
        ),
    ]
