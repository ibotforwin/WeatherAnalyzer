# Generated by Django 3.0.5 on 2020-09-02 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_auto_20200902_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadeddocument',
            name='file_name',
        ),
    ]
