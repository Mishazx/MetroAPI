import datetime
from traceback import format_tb
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from .models import Location, Station, Train, Wagon

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
    # search_fields = ('id', 'line', 'way', 'arrival_time', 'train_index')
    
    def prev_station_name(self, obj):
        if obj.prev_station:
            url = reverse('admin:TrainAPI_station_change', args=[obj.prev_station.id])
            return format_html('<a href="{}">{}</a>', url, obj.prev_station.name_ru)
        return obj.prev_station.name_ru
    def next_station_name(self, obj):
        if obj.next_station:
            url = reverse('admin:TrainAPI_station_change', args=[obj.next_station.id])
            return format_html('<a href="{}">{}</a>', url, obj.next_station.name_ru)
        return obj.next_station.name_ru
    
    prev_station_name.admin_order_field = 'prev_station__name_ru'
    next_station_name.admin_order_field = 'next_station__name_ru'
    
    # def prev_station_name(self, obj):
    #     if obj.prev_station:
    #         url = reverse('admin:TrainAPI_prev_station', args=[obj.prev_station.name_ru])
    #         return format_tb('<a href="{}">{}</a>', url, obj.prev_station.name_ru)
        
    #     return obj.prev_station.name_ru 
    # def next_station_name(self, obj):
    #     return obj.next_station.name_ru
    
    # prev_station_name.admin_order_field = 'prev_station__prev_station_name'

    


class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'lineId', 'name_ru', 'name_en', 'location')
    list_filter = ('lineId',)
    search_fields = ('name_ru', 'name_en')


from django.contrib.auth.models import User
from django.http import HttpResponse

class UserAdmin(admin.ModelAdmin):
    actions = ['toggle_celery_task_enabled']
    def toggle_celery_task_enabled(self, request, queryset):
        settings.CELERY_MAIN_TASK_ENABLED = not settings.CELERY_MAIN_TASK_ENABLED
        return HttpResponse('Celery main task enabled: {}'.format(settings.CELERY_MAIN_TASK_ENABLED))
    toggle_celery_task_enabled.short_description = 'Toggle Celery main task enabled'
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# def toggle_celery_task_enabled(modeladmin, request, queryset):
#     settings.CELERY_MAIN_TASK_ENABLED = not settings.CELERY_MAIN_TASK_ENABLED
#     return HttpResponse('Celery main task enabled: {}'.format(settings.CELERY_MAIN_TASK_ENABLED))

# toggle_celery_task_enabled.short_description = 'Toggle Celery main task enabled'


# admin.site.add_action(toggle_celery_task_enabled, 'toggle_celery_task_enabled')



class LocationAdmin(admin.ModelAdmin):
    list_display = ('lat', 'lon')
    list_filter = ('lat', 'lon')
    search_fields = ('lat', 'lon')


admin.site.register(Location, LocationAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(Train, TrainAdmin)
admin.site.register(Wagon, WagonAdmin)