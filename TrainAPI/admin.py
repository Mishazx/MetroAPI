import datetime
from django.contrib import admin
from .models import Station, Train, Wagon

from django.utils.translation import gettext_lazy as _

class FiveMinutesAgoFilter(admin.SimpleListFilter):
    title = _('Modified in last 5 minutes')
    parameter_name = 'odified_in_last_5_minutes'
    def lookups(self, request, model_admin):
        return (
        ('yes', _('Yes')),
        )
    def queryset(self, request, queryset):
        now = datetime.datetime.now()
        five_minutes_ago = now - datetime.timedelta(minutes=5)
        return queryset.filter(modification_time__gte=five_minutes_ago)

class WagonAdmin(admin.ModelAdmin):
    list_display = ('number', 'wagon_type', 'train')
    list_filter = ('train',)


class TrainAdmin(admin.ModelAdmin):
    list_display = ('id', 'line', 'way', 'prev_station_name', 'next_station_name', 'arrival_time', 'train_index', 'modification_time')
    list_filter = ('line', 'way', 'modification_time', 
                #    FiveMinutesAgoFilter
                   )
    search_fields = ('id', 'line', 'way', 'arrival_time', 'train_index')
    def prev_station_name(self, obj):
        return obj.prev_station.name_ru 
    def next_station_name(self, obj):
        return obj.next_station.name_ru

    


class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'lineId', 'name_ru', 'name_en')
    list_filter = ('lineId',)
    search_fields = ('name_ru', 'name_en')


admin.site.register(Station, StationAdmin)
admin.site.register(Train, TrainAdmin)
admin.site.register(Wagon, WagonAdmin)