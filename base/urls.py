from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dates=30d', views.get_data30, name='dates=30d'),
    path('chart', views.get_data, name='chart'),
]