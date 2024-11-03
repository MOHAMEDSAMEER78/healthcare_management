# Generated by Django 5.1.2 on 2024-11-03 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PatientData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('edge_device_name', models.CharField(blank=True, max_length=100)),
                ('age', models.IntegerField()),
                ('heartrate', models.IntegerField(blank=True, null=True)),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('blood_pressure', models.CharField(blank=True, max_length=20)),
                ('glucose_level', models.FloatField(blank=True, null=True)),
                ('oxygen_level', models.FloatField(blank=True, null=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
    ]
