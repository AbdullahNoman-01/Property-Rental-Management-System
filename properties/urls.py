from django.urls import path
from . import views


urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('create/',views.property_create,name='property_create'),
    path('<int:pk>/',views.property_detail,name='property_detail'),
    path('<int:pk>/edit/',views.property_update,name='property_update'),
    path('<int:pk>/delete/',views.property_delete,name='property_delete'),
    path(
        '<int:property_id>/request/',
        views.create_rental_request,
        name='create_rental_request'
    ),

    path(
        'my-rental-requests/',
        views.my_rental_requests,
        name='my_rental_requests'
    ),

    path(
        'rental-request/<int:request_id>/cancel/',
        views.cancel_rental_request,
        name='cancel_rental_request'
    ),

    path(
        'owner/rental-requests/',
        views.owner_rental_requests,
        name='owner_rental_requests'
    ),

    path(
        'rental-request/<int:request_id>/accept/',
        views.accept_rental_request,
        name='accept_rental_request'
    ),

    path(
        'rental-request/<int:request_id>/reject/',
        views.reject_rental_request,
        name='reject_rental_request'
    ),
    path('notifications/',views.notifications,name='notifications'),
    path(
        'notifications/<int:notification_id>/',
        views.notification_redirect,
        name='notification_redirect'
    ),
    path(
        'notifications/mark-all-read/',
        views.mark_all_notifications_read,
        name='mark_all_notifications_read'
    ),
]