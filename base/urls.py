from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('date30d', views.date30d, name='date30d'),
    path('date14d', views.date14d, name='date14d'),
    path('date7d', views.date7d, name='date7d'),
    path('chart', views.get_data, name='chart'),
    path('chart2', views.get_data30, name='chart2'),
    path('chart3', views.get_data14, name='chart3'),
    path('chart4', views.get_data7, name='chart4'),
]
