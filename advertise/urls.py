from django.urls import path
from . import views

app_name = 'advertise'

urlpatterns = [
    path('', views.advertise_view, name='advertise'),
]
