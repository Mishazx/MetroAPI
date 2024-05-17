from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('station/<int:station_id>/', views.request_station_view, name='request_station'),
    path('stations/generation/', views.GenerationListStation, name='generationListStation'),
    path('train/<int:station_id>/', views.update_train, name='updateTrain'),
    path('trains/', views.update, name='update'),
    path('get_moscow_msg/', views.get_moscow_msg, name='getMoscow'),
    path('get_count_moscow_msg/', views.get_count_moscow_msg, name='getCountMoscow'),
    
    # path('stations/get/', views.GetListStation, name='getListStation'),
]
