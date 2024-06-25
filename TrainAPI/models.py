from django.db import models


class Wagon(models.Model):
    train = models.ForeignKey('Train', on_delete=models.CASCADE)
    number = models.IntegerField() # номер вагона (0-7)
    wagon_type = models.CharField(max_length=100) # тип вагона


class Train(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    line = models.IntegerField()
    way = models.CharField(max_length=100)
    prev_station = models.ForeignKey('Station', related_name='prev_stations', on_delete=models.CASCADE)
    next_station = models.ForeignKey('Station', related_name='next_stations', on_delete=models.CASCADE)
    arrival_time = models.IntegerField()
    train_index = models.IntegerField()

    modification_time = models.DateTimeField(auto_now=True)


class Station(models.Model):
    id = models.IntegerField(primary_key=True)
    lineId = models.IntegerField()
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True)
    
class Location(models.Model):
    lat = models.DecimalField(max_digits=16, decimal_places=12)
    lon = models.DecimalField(max_digits=16, decimal_places=12)