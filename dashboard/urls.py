from django.urls import path
from . import views


urlpatterns = [
    path(
        'owner/',
        views.owner_dashboard,
        name='owner_dashboard'
    ),

    path(
        'tenant/',
        views.tenant_dashboard,
        name='tenant_dashboard'
    ),
]