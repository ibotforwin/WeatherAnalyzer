# Generated by Django 3.0.5 on 2020-09-03 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_auto_20200902_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherdatarow',
            name='speed_max_gusts',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]