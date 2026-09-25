from django.urls import path
from . import views

app_name = 'about_us'

urlpatterns = [
    path('', views.about_us_view, name='about_us'),
]
