# Generated by Django 5.0.6 on 2024-05-08 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('line', models.IntegerField()),
                ('way', models.CharField(max_length=100)),
                ('prev_station', models.IntegerField()),
                ('next_station', models.IntegerField()),
                ('arrival_time', models.IntegerField()),
                ('train_index', models.IntegerField()),
                ('wagon0', models.CharField(max_length=100)),
                ('wagon1', models.CharField(max_length=100)),
                ('wagon2', models.CharField(max_length=100)),
                ('wagon3', models.CharField(max_length=100)),
                ('wagon4', models.CharField(max_length=100)),
                ('wagon5', models.CharField(max_length=100)),
                ('wagon6', models.CharField(max_length=100)),
                ('wagon7', models.CharField(max_length=100)),
                ('modification_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
