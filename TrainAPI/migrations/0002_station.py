# Generated by Django 5.0.6 on 2024-05-08 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrainAPI', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('lineId', models.IntegerField()),
                ('name_ru', models.CharField(blank=True, max_length=100, null=True)),
                ('name_en', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
