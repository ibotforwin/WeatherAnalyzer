# Generated by Django 3.0.5 on 2020-09-02 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateField()),
                ('min_temp', models.FloatField()),
                ('max_temp', models.FloatField()),
                ('mean_temp', models.FloatField()),
                ('heat_degree_days', models.FloatField()),
                ('total_rain', models.FloatField()),
                ('total_snow', models.FloatField()),
                ('speed_max_gusts', models.FloatField()),
            ],
        ),
    ]
