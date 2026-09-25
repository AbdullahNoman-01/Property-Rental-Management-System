from django.urls import path
from . import views


urlpatterns = [
    path(
        'property/<int:property_id>/review/',
        views.create_review,
        name='create_review'
    ),
]